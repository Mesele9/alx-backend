#!/usr/bin/env python3
""" 0-basic-cache.py """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """a class that inherits from BaseCaching and is a chaching system
    """
    def put(self, key, item):
        """ Add items to the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Get item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
