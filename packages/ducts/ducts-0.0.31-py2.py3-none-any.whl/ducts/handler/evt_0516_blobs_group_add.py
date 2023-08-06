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
local group_name_with_key = ARGV[2];
local stream_id = redis.call("XADD", redis_key_group_metadata, "*", unpack(ARGV, 3, table.maxn(ARGV)));
redis.call("ZADD", redis_key_group_names, 0, group_name_with_key);
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
        return await self.add_group(event.session, **event.data[0])

    async def add_group(self, session : EventSession, group_name : str = '', content_type : str = '', **other_params):
        metadata = self.helper.GroupMetadata(other_params.copy())
        metadata.group_name = group_name if group_name else ''
        metadata.content_type = content_type if content_type else 'application/octet-stream'

        metadata.gid = await session.redis.execute('INCR', self.helper.incr_key_for_group_id())
        metadata.group_key = hashlib.md5(struct.pack('i', metadata.gid)+struct.pack('d', datetime.now().timestamp())).hexdigest()
        
        redis_key_group_metadata = self.helper.stream_key_for_group_metadata(metadata.group_key)
        redis_key_group_names = self.helper.zset_key_for_group_names()

        ret = await session.redis.evalsha(
            Handler.SCRIPT
            , 2
            , redis_key_group_metadata, redis_key_group_names
            , metadata.group_key, '{}::{}'.format(metadata.group_name,metadata.group_key), *chain.from_iterable(metadata.items()))
        return metadata.group_key
            


