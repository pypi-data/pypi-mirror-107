from ducts.spi import EventHandler, webapi

from io import BytesIO
from hashlib import md5
from datetime import datetime

from aiohttp import web


import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager
        self.helper = manager.load_helper_module('helper_blobs')
        handler_spec.set_description('Get Value from Redis Server')
        return handler_spec

    async def run(self, manager):
        self.list_groups = self.manager.get_handler_for(510)[1].list_groups
        self.list_contents = self.manager.get_handler_for(520)[1].list_contents
        self.list_content_versions = self.manager.get_handler_for(521)[1].list_versions
        self.list_content_metadata = self.manager.get_handler_for(522)[1].get_metadata
        self.get_group_metadata = self.manager.get_handler_for(512)[1].get_metadata
        
    async def handle(self, event):
        call = self.get_content
        if isinstance(event.data, str):
            raise ValueError('both group_key and content_key are required.')
        elif isinstance(event.data, list):
            coro = call(*event.data)
        elif isinstance(event.data, map):
            coro = call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            raise ValueError('both group_key and content_key are required.')
        content_metadata, data_length = await coro.__anext__()
        async for ret in coro:
            yield ret

    async def get_content(self, group_key : str, content_key : str, version : str = '', start : int = 0, stop : int = -1):
        if version:
            group, content, version = await self.helper.get_group_content_metadata_for(
                self.manager.redis, group_key, content_key, version)
        else:
            group, content, version = await self.helper.get_group_content_metadata_with_version(
                self.manager.redis, group_key, content_key)

        redis_key_blob_data = self.helper.obj_key_for_content(group.gid,  content.cid)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_blob_data)
        if content_length != int(content.content_length):
            #load from other locations
            pass

        if start == 0 and stop == -1:
            data = await self.manager.redis.execute('GET', redis_key_blob_data)
        elif start > content_length:
            raise ValueError('RequestRangeNotSatisfiable. length=[{}] but start was [{}]'.format(content_length, start))
        else:
            data = await self.manager.redis.execute('GETRANGE', redis_key_blob_data, start, stop)

        yield (content, len(data))
        
        bio = BytesIO(data)
        for buf in iter(lambda: bio.read(1024*1024), b''):
            yield buf
        yield b''
        
    @webapi.add_route(path='/groups', method='GET')
    async def group_keys(self, request):
        ret = await self.list_groups()
        return web.json_response(ret)
    
    @webapi.add_route(path='/groups/{group_key}/contents', method='GET')
    async def content_keys(self, request):
        group_key = request.match_info['group_key']
        try:
            ret = await self.list_contents(group_key)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/versions', method='*')
    async def content_versions(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        try:
            ret = await self.list_content_versions(group_key, content_key)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()
        
    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/metadata', method='*')
    async def content_metadata(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        try:
            ret = await self.list_content_metadata(group_key, content_key)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()

    @webapi.add_route(path='/groups/{group_key}/contents/{content_key}/versions/{version}/metadata', method='*')
    async def content_metadata_of(self, request):
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']
        version = request.match_info['version']
        try:
            ret = await self.list_content_metadata(group_key, content_key, version)
            return web.json_response(ret)
        except KeyError as e:
            raise web.HTTPNotFound()
    
    @webapi.add_route(path='/{group_key}/{content_key}/blob', method='*')
    async def service(self, request):
        logger.debug('HEADERS|%s', request.raw_headers)
        group_key = request.match_info['group_key']
        content_key = request.match_info['content_key']

        group, content, version = await self.helper.get_group_content_metadata_with_version(
            self.manager.redis, group_key, content_key)

        redis_key_blob_data = self.helper.obj_key_for_content(group.gid,  content.cid)
        content_length = await self.manager.redis.execute('STRLEN', redis_key_blob_data)
        if content_length != int(content.content_length):
            #load from other locations
            pass

        content_range = None
        if request.http_range is None or (request.http_range.start == request.http_range.stop == None):
            http_status = 200
            data = await self.manager.redis.execute('GET', redis_key_blob_data)
        elif request.http_range.start > content_length:
            err = web.HTTPRequestRangeNotSatisfiable()
            err.headers['Content-Range'] = 'bytes {}'.format(content_length)
            raise err
        else:
            http_status = 206
            start = request.http_range.start if request.http_range.start is not None else 0
            stop = request.http_range.stop -1 if request.http_range.stop is not None else content_length - 1
            data = await self.manager.redis.execute('GETRANGE', redis_key_blob_data, start, stop)
            content_range = "bytes {}-{}/{}".format(start, stop, content_length)

        data_length = len(data)
        response = web.StreamResponse(status=http_status)
        response.content_type = content.content_type
        response.content_length = data_length
        response.headers['Accept-Ranges'] = 'bytes'
        if content_range is not None:
            response.headers['Content-Range'] = content_range
        response.headers['ETag'] = content.md5
        await response.prepare(request)

        print(response.headers)

        bio = BytesIO(data)
        for buf in iter(lambda: bio.read(1024*1024), b''):
            await response.write(buf)
        await response.write_eof()




    
