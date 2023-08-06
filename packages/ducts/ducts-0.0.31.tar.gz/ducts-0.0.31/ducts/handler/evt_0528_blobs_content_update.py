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
local content_key = ARGV[1];
local content_order = ARGV[2];
local content = ARGV[3];
redis.call("SET", redis_key_contents_object, content);
local stream_id = redis.call("XADD", redis_key_contents, "*", unpack(ARGV, 4, table.maxn(ARGV)));
redis.call("ZADD", redis_key_contents_keys, content_order, content_key);
return stream_id;
'''
    
    SCRIPT_METADATA_ONLY='''\
local redis_key_contents = KEYS[1];
local redis_key_contents_keys = KEYS[2];
local content_key = ARGV[1];
local content_order = ARGV[2];
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
            , content_body : bytes
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
        
        if not content_body:
            if old == content:
                return version
            else:
                ret = await session.redis.evalsha(
                    Handler.SCRIPT_METADATA_ONLY
                    , 2
                    , redis_key_contents_metadata, redis_key_contents_keys
                    , content.content_key, content.order, *chain.from_iterable(content.items()))
                return {'group_key': group.group_key, 'content_key': content.content_key, 'version': ret.decode('UTF-8')}

        if isinstance(content_body, str):
            content.encoding = content.encoding if content.encoding else 'UTF-8'
            content_body = content_body.encode(content.encoding)
        elif not isinstance(content_body, bytes):
            raise ValueError('content_body must be str or bytes but was {}'.format(type(content_body)))
    
        content.content_length = len(content_body)
        content.md5 = hashlib.md5(content_body).hexdigest()

        if old.last_modified == content.last_modified:
            content.last_modified = int(datetime.now().timestamp())
        else:
            content.last_modified = self.helper.determine_last_modified(content.last_modified)
        
        content.cid = await session.redis.execute('INCR', self.helper.incr_key_for_content_id(group.gid))

        redis_key_contents_object = self.helper.obj_key_for_content(group.gid, content.cid)

        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 3
            , redis_key_contents_metadata, redis_key_contents_object, redis_key_contents_keys
            , content.content_key, content.order, content_body, *chain.from_iterable(content.items()))
        return {'group_key': group.group_key, 'content_key': content.content_key, 'version': ret.decode('UTF-8')}
        
