
from datetime import datetime
from email.utils import parsedate_to_datetime

import asyncio

from ducts import utils
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)
        
@config_callback
def config(loader):
    pass

conf = configure_module(config)

GroupMetadata = utils.nameddict(
    'GroupMetadata',
    (
        'gid'
        , 'group_key'
        , 'group_name'
        , 'content_type'
    ))

ContentMetadata = utils.nameddict(
    'ContentMetadata',
    (
        'cid'
        , 'content_key'
        , 'content_name'
        , 'content_type'
        , 'content_length'
        , 'last_modified'
        , 'encoding'
        , 'md5'
        , 'order'
        , 'revert_to'
    ))

def incr_key_for_group_id():
    return f'BLOBS/GROUP_ID'

def zset_key_for_group_names():
    return f'BLOBS/GROUP_NAMES'

def stream_key_for_group_metadata(group_key):
    return f'BLOBS/GKEY={group_key}/METADATA'


def incr_key_for_content_id(group_id):
    return f'BLOBS/GID={group_id}/CONTENT_ID'

def zset_key_for_content_keys(group_id):
    return f'BLOBS/GID={group_id}/CONTENT_KEYS'

#def stream_key_for_contents_metadata(group_id):
#    return f'BLOBS/GID={group_id}/CONTENTS_METADATA'

#def list_key_for_versions(group_id, content_key):
#    return f'BLOBS/GID={group_id}/CKEY={content_key}/VERSIONS'

def stream_key_for_contents_metadata(group_id, content_key):
    return f'BLOBS/GID={group_id}/CKEY={content_key}/METADATA'

def obj_key_for_content(group_id, content_id):
    return f'BLOBS/GID={group_id}/CID={content_id}/OBJ'

def stream_key_for_object_buffer():
    return 'BLOBS/BUFFER'

def obj_key_for_object_buffer(session_id, buffer_id):
    return f'BLOBS/BUFFER/{session_id}/{buffer_id}'



async def get_group_metadata_with_version(redis, group_key):
    stream_key = stream_key_for_group_metadata(group_key)
    stream_id, kv = await redis.xlast_str_with_id(stream_key)
    if not stream_id:
        raise KeyError('group_key[{}] not found.'.format(group_key))
    return (GroupMetadata(kv), stream_id)

async def get_group_metadata(redis, group_key):
    stream_key = stream_key_for_group_metadata(group_key)
    kv = await redis.xlast_str(stream_key)
    if not kv:
        raise KeyError('group_key[{}] not found.'.format(group_key))
    return GroupMetadata(kv)

async def get_group_content_metadata_with_version(redis, group_key, content_key):
    group = await get_group_metadata(redis, group_key)
    
    stream_key = stream_key_for_contents_metadata(group.gid, content_key)
    stream_id, kv = await redis.xlast_str_with_id(stream_key)
    if not stream_id:
        raise KeyError('content_key [{}/{}] not found.'.format(group_key, content_key))
    return (group, ContentMetadata(kv), stream_id)
    
async def get_group_content_metadata_for(redis, group_key, content_key, version):
    group = await get_group_metadata(redis, group_key)

    stream_key = stream_key_for_contents_metadata(group.gid, content_key)
    ret_version, content_dict = await redis.xget_str_with_id(stream_key, version)
    content = ContentMetadata(content_dict)
    if not content or content.content_key != content_key:
        raise KeyError('version[{}] not found in content_key [{}/{}]'.format(version, group_key, content_key))
    return (group, content, ret_version)

def determine_last_modified(last_modified_in_request):
    if not last_modified_in_request:
        try:
            dt = datatime.fromtimestamp(int(last_modified_in_request))
        except ValueError:
            dt = parsedate_to_datetime(last_modified_in_request)
    else:
        dt = datetime.now()
        #last_modified = formatdate(timeval=None, localtime=False, usegmt=True)
    return int(dt.timestamp())
