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
local redis_key_group_metadata = KEYS[1];
local redis_key_group_names = KEYS[2];
local group_key = ARGV[1];
local group_name_with_key_new = ARGV[2];
local group_name_with_key_old = ARGV[3];
local stream_id = redis.call("XADD", redis_key_group_metadata, "*", unpack(ARGV, 4, table.maxn(ARGV)));
redis.call("ZREM", redis_key_group_names, group_name_with_key_old);
redis.call("ZADD", redis_key_group_names, 0, group_name_with_key_new);
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
        return await self.update_group(event.session, **event.data)

    async def update_group(self, session : EventSession, group_key : str = '', gid : str = '', **update_params):
        if not group_key:
            raise ValueError('group_key is required.')
        
        metadata, version = await self.helper.get_group_metadata_with_version(self.manager.redis, group_key)
        old = metadata.copy()
        
        if gid and gid != metadata.gid:
            raise ValueError('gid was expeccted to be [{}] but was [{}].'.format(metadata.gid, gid))

        metadata.update(update_params)

        if old == metadata:
            return version

        redis_key_group_metadata = self.helper.stream_key_for_group_metadata(group_key)
        
        if old.group_name == metadata.group_name:
            return await self.manager.redis.xadd(redis_key_group_metadata, **metadata)
        else:
            redis_key_group_names = self.helper.zset_key_for_group_names()
            ret = await session.redis.evalsha(
                Handler.SCRIPT
                , 2
                , redis_key_group_metadata, redis_key_group_names
                , metadata.group_key, '{}::{}'.format(metadata.group_name,metadata.group_key), '{}::{}'.format(old.group_name,metadata.group_key), *chain.from_iterable(metadata.items()))
            return metadata.group_key
