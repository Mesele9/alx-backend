#!/usr/bin/env python3
""" 2-lifo_cache.py """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ a LIFO cache that inherits from BaseCaching """
    def __init__(self):
        """ Initialize the LIFO cache """
        super().__init__()
        self.lifo_order = []

    def put(self, key, item):
        """ Add item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.lifo_order:
                    last_key = self.lifo_order.pop()
                    print("DISCARD: {}".format(last_key))
                    del self.cache_data[last_key]
            self.cache_data[key] = item
            self.lifo_order.append(key)

    def get(self, key):
        """ Get item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
