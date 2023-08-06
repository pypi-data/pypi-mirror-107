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
local content_key = ARGV[1];
local content_order = ARGV[2];
local content = ARGV[3];
redis.call("SET", redis_key_contents_object, content);
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 4, table.maxn(ARGV)));
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
            , content : bytes
            , content_name : str = ''
            , content_type : str = ''
            , encoding : str =''
            , last_modified : str = ''
            , order : int = ''
            , **other_params):
        if not group_key:
            raise ValueError('group_key must be set')
        if not content:
            raise ValueError('content must be set')

        group = await self.helper.get_group_metadata(self.manager.redis, group_key)
        
        metadata = self.helper.ContentMetadata(other_params.copy())
        metadata.content_name = content_name if content_name else ''

        guessed = guess_type(content_name)[0]
        if isinstance(content, str):
            guessed = guessed if guessed else 'text/plain'
            metadata.content_type = content_type if content_type else guessed
            encoding = encoding if encoding else 'UTF-8'
            metadata.encoding = encoding
            content = content.encode(encoding)
        elif isinstance(content, bytes):
            guessed = guessed if guessed else 'application/octet-stream'
            metadata.content_type = content_type if content_type else guessed
            if encoding:
                metadata.encoding = encoding
        else:
            raise ValueError('content must be str or bytes but was {}'.format(type(content)))

        metadata.content_length = len(content)
        metadata.md5 = hashlib.md5(content).hexdigest()

        metadata.last_modified = self.helper.determine_last_modified(last_modified)
        metadata.cid = await session.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))
        metadata.order = order if order else metadata.cid * 10

        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, metadata.cid)
        metadata.content_key = hashlib.md5(redis_key_contents_object.encode('UTF-8')).hexdigest()
        
        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, metadata.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)

        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 3
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys
            , metadata.content_key, metadata.order, content, *chain.from_iterable(metadata.items()))
        return {'group_key': group.group_key, 'content_key': metadata.content_key}
            


