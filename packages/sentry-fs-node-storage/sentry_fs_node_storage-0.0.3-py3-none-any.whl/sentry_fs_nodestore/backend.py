import gzip
import math
import os
from datetime import datetime, timedelta

import zstandard as zstd
from django.utils import timezone

from sentry.nodestore.base import NodeStorage
from sentry.nodestore.bigtable import json_loads, json_dumps


class FSNodeStorage(NodeStorage):
    compressor = zstd.ZstdCompressor()
    decompressor = zstd.ZstdDecompressor()

    def __init__(self, base_path="/data/nodestore/"):
        self.base_path = base_path

    def _get_path(self, id):
        return os.path.join(self.base_path, id[:2], id[2:4], id[4:])

    def _decompress(self, data):
        if data[:2] == b'\x1f\x8b':
            return gzip.decompress(data)
        return self.decompressor.decompress(data)

    def delete(self, id):
        try:
            os.remove(self._get_path(id))
        except FileNotFoundError:
            pass
        self._delete_cache_item(id)

    def get(self, id):
        item_from_cache = self._get_cache_item(id)
        if item_from_cache:
            return item_from_cache
        try:
            with open(self._get_path(id), 'rb') as fp:
                data = fp.read()
            data = json_loads(self._decompress(data).decode('utf-8'))
        except FileNotFoundError:
            return None
        else:
            self._set_cache_item(id, data)
            return data

    def get_multi(self, id_list):
        cache_items = self._get_cache_items(id_list)
        if len(cache_items) == len(id_list):
            return cache_items

        items = {}
        uncached_ids = [id for id in id_list if id not in cache_items]
        for id in uncached_ids:
            try:
                with open(self._get_path(id), 'rb') as fp:
                    data = fp.read()
            except FileNotFoundError:
                items[id] = None
            else:
                data = json_loads(self._decompress(data).decode('utf-8'))
                items[id] = data
        self._set_cache_items(items)
        items.update(cache_items)
        return items

    def delete_multi(self, id_list):
        for id in id_list:
            try:
                os.remove(self._get_path(id))
            except FileNotFoundError:
                pass
        self._delete_cache_items(id_list)

    def set(self, id, data, ttl=None):
        path = self._get_path(id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = self.compressor.compress(json_dumps(data).encode("utf-8"))
        with open(path, "wb") as f:
            f.write(data)
        self._set_cache_item(id, data)

    def cleanup(self, cutoff_timestamp):
        total_seconds = (timezone.now() - cutoff_timestamp).total_seconds()
        days = math.floor(total_seconds / 86400)

        today = datetime.today()
        for root, directories, files in os.walk(self.base_path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    filetime = os.stat(path).st_mtime
                    if filetime < (today - timedelta(days=days)).timestamp():
                        os.remove(path)

        if self.cache:
            self.cache.clear()

    def bootstrap(self):
        # Nothing for Django backend to do during bootstrap
        pass
