import json

from b2_browser.settings import B2_API_ID, B2_API_KEY, B2_BUCKET, DEBUG
from b2sdk.v1 import InMemoryAccountInfo
from b2sdk.v1 import B2Api
from django.core.cache import cache
import datetime
import os

_info = InMemoryAccountInfo()

_api_obj = B2Api(_info)
_api_obj.authorize_account('production', B2_API_ID, B2_API_KEY)


def b2ls(path=''):
    a = cache.get(f'path:{path}')

    if a is not None:
        return json.loads(a)

    # Get a list of file / folders
    obj = []

    b = _api_obj.get_bucket_by_name(B2_BUCKET)

    for f_info, fn in b.ls(show_versions=False, folder_to_list=path, recursive=False):
        entry = {}

        if fn is not None:
            entry['is_file'] = False
            entry['name'] = fn
            entry['friendly_name'] = os.path.basename(os.path.normpath(fn))
        else:
            entry['is_file'] = True
            entry['name'] = f_info.file_name
            entry['friendly_name'] = os.path.basename(os.path.normpath(f_info.file_name))
            entry['size'] = f_info.size
            if f_info.content_type is not None:
                entry['type'] = f_info.content_type.split(";")[0]
            else:
                entry['type'] = "Unknown"
            if f_info.content_sha1 is not None and f_info.content_sha1 != "none":
                entry['sha1'] = f_info.content_sha1
            else:
                entry['sha1'] = "Unknown"
            if f_info.upload_timestamp is not None:
                entry['time'] = str(datetime.datetime.utcfromtimestamp(f_info.upload_timestamp / 1000))

        obj.append(entry)

    cache.set(f'path:{path}', json.dumps(obj), timeout=(60 * 60 * 24))

    return obj
