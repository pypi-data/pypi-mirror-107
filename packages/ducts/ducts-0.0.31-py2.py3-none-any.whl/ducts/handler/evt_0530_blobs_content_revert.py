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
        return await self.revert_content(event.session, event.data[0], event.data[1], event.data[2])

    async def revert_content(
            self
            , session : EventSession
            , group_key : str
            , content_key : str
            , to_version : str):
        
        if not group_key:
            raise ValueError('group_key must be set')
        if not content_key:
            raise ValueError('content_key must be set')
        if not to_version:
            raise ValueError('to_version must be set')

        
        group, to_content, to_version = await self.helper.get_group_content_metadata_for(
            self.manager.redis, group_key, content_key, to_version)
        
        group, from_content, from_version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, group_key, content_key)

        if to_content == from_content:
            return to_version

        if from_content.content_key != to_content.content_key:
            raise ValueError('content_key was expeccted to be [{}] but was [{}].'.format(to_content.content_key, from_content.content_key))

        if not to_content.revert_to:
            to_content.revert_to = to_version

        redis_key_contents_metadata = self.helper.stream_key_for_contents_metadata(group.gid, to_content.content_key)
        redis_key_contents_keys = self.helper.zset_key_for_content_keys(group.gid)
        
        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 2
            , redis_key_contents_metadata, redis_key_contents_keys
            , to_content.content_key, to_content.order, *chain.from_iterable(to_content.items()))
        return {'group_key': group.group_key, 'content_key': to_content.content_key, 'version': ret.decode('UTF-8')}

