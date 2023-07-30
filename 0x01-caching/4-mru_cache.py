#!/usr/bin/env python3
""" 4-mru_cache.py """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ a Most Recently Used cache class that inherits from BaseCaching """
    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.mru_order = []

    def put(self, key, item):
        """ Add an item in the the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.mru_order:
                    mru_key = self.mru_order.pop()
                    print("DISCARD: {}".format(mru_key))
                    del self.cache_data[mru_key]
            self.cache_data[key] = item
            self.mru_order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.mru_order.remove(key)
            self.mru_order.append(key)
            return self.cache_data[key]
        return None
