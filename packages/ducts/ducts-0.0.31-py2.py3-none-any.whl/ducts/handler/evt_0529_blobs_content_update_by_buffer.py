from ducts.spi import EventHandler, EventSession

from io import BytesIO
from datetime import datetime
from itertools import chain
import math
import hashlib
import struct

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
        return await self.update_content(event.session, event.data[0], event.data[1], event.data[2], event.data[3] if len(event.data) > 3 else {})

    async def update_content(
            self
            , session : EventSession
            , group_key : str
            , content_key : str
            , content_buffer_key : str
            , update_params : dict = {}):
        
        if not group_key:
            raise ValueError('group_key must be set')
        if not content_key:
            raise ValueError('content_key must be set')
        if not isinstance(update_params, dict):
            raise ValueError('update_dict must be an instance of dict')
        
        group, content, version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, group_key, content_key)
        
        old = content.copy()
        content.update(update_params)

        if content.cid != old.cid:
            raise ValueError('cid was expeccted to be [{}] but was [{}].'.format(old.cid, content.cid))

        if content.content_key != old.content_key:
            raise ValueError('content_key was expeccted to be [{}] but was [{}].'.format(old.content_key, content.content_key))

        if (content.content_name != old.content_name) and (content.content_type == old.content_type):
            guessed = guess_type(content.content_name)[0]
            content.content_type = guessed if guessed else content.content_type

        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, content.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)
        
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
            
        content.content_length = content_length
        content.md5 = md5.hexdigest()
            
        if old.last_modified == content.last_modified:
            content.last_modified = int(datetime.now().timestamp())
        else:
            content.last_modified = self.helper.determine_last_modified(content.last_modified)
        
        content.cid = await session.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))

        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, content.cid)

        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 4
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys, redis_key_contents_object_buffer
            , content.content_key, content.order, *chain.from_iterable(content.items()))
        return {'group_key': group.group_key, 'content_key': content.content_key, 'version': ret.decode('UTF-8')}
    
