#!/usr/bin/env python3
""" 100-lfu_cache.py """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ Least Frequently used cache class that inhertits from BaseCaching """
    def __init__(self):
        """ Inititlize the cache """
        super().__init__()
        self.frequency = {}
        self.frequency_lists = {1: []}
        self.min_frequency = 1

    def put(self, key, item):
        """ add item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency[key] += 1
                self.frequency_lists[self.frequency[key] - 1].remove(key)
                if not self.frequency_lists[self.frequency[key] - 1]:
                    del self.frequency_lists[self.frequency[key] -1]

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                while not self.frequency_lists[self.min_frequency]:
                    self.min_frequency += 1

                lfu_key = self.frequency_lists[self.min_frequency].pop(0)
                print("DISCARD: {}".format(lfu_key))
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.frequency_lists[1].append(key)
            self.min_frequency = 1

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.frequency[key] += 1
            self.frequency_lists[self.frequency[key] - 1].remove(key)
            if not self.frequency_lists[self.frequency[key] -1]:
                del self.frequency_lists[self.frequency[key] - 1]
            if self.frequency[key] not in self.frequency_lists:
                self.frequency_lists[self.frequency[key]] = []
            self.frequency_lists[self.frequency[key]].append(key)
            return self.cache_data[key]
        return None
