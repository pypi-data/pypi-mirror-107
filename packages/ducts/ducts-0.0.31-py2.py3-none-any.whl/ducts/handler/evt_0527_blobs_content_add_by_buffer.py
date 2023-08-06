from ducts.spi import EventHandler, EventSession

from io import BytesIO
from datetime import datetime
from struct import pack
from itertools import chain
import math
import hashlib

from mimetypes import guess_type
from email.utils import formatdate
from email.utils import parsedate_to_datetime

from aiohttp import web

import traceback
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    SCRIPT='''\
local redis_key_contents = KEYS[1];
local redis_key_contents_object = KEYS[2];
local redis_key_contents_keys = KEYS[3];
local redis_key_contents_object_buffer = KEYS[4];
local content_key = ARGV[1];
local content_order = ARGV[2];
redis.call("RENAME", redis_key_contents_object_buffer, redis_key_contents_object);
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 3, table.maxn(ARGV)));
redis.call("ZADD", redis_key_contents_keys, content_order, content_key);
return stream_id;
'''

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')

        handler_spec.set_description('Register Resource')
        return handler_spec

    async def handle(self, event):
        return await self.add_content(event.session, event.data[0], event.data[1], **event.data[2])

    async def add_content(
            self
            , session : EventSession
            , group_key : str
            , content_buffer_key : str
            , content_name : str = ''
            , content_type : str = ''
            , encoding : str =''
            , last_modified : str = ''
            , order : int = ''
            , **other_params):
        if not group_key:
            raise ValueError('group_key must be set')
        if not content_buffer_key:
            raise ValueError('content_buffer_key must be set')
        if not isinstance(content_buffer_key, str):
            raise ValueError('content_buffer_key mus be string but was {}'.format(type(content)))

        group = await self.helper.get_group_metadata(self.manager.redis, group_key)
        guessed = guess_type(content_name)[0]
        
        metadata = self.helper.ContentMetadata(other_params.copy())
        metadata.content_name = content_name if content_name else ''
        metadata.content_type = content_type if content_type else guessed
        if encoding:
            metadata.encoding = encoding

        redis_key_contents_object_buffer = self.helper.obj_key_for_object_buffer(session.session_id(), content_buffer_key)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_contents_object_buffer)
        md5 = hashlib.md5()
        #sha256 = hashlib.sha256()
        #buf_len = int(md5.block_size * sha256.block_size / math.gcd(md5.block_size, sha256.block_size)) * 4096
        buf_len = md5.block_size * 4096
        start = 0
        while start <= content_length:
            end = start + buf_len - 1
            buf = await self.manager.redis.execute('GETRANGE', redis_key_contents_object_buffer, start, end)
            md5.update(buf)
            #sha256.update(buf)
            start += buf_len
            
        metadata.content_length = content_length
        metadata.md5 = md5.hexdigest()

        metadata.last_modified = self.helper.determine_last_modified(last_modified)
        metadata.cid = await session.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))
        metadata.order = order if order else metadata.cid * 10

        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, metadata.cid)
        metadata.content_key = hashlib.md5(redis_key_contents_object.encode('UTF-8')).hexdigest()

        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, metadata.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)

        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 4
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys, redis_key_contents_object_buffer
            , metadata.content_key, metadata.order, *chain.from_iterable(metadata.items()))
        return {'group_key': group.group_key, 'content_key': metadata.content_key}
            


