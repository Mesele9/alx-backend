#!/usr/bin/env python3
""" Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """ a function that takes two integer arguments page and page_size, and
    return a tuple of size two containing a start index and an end index.
    """
    if page <= 1:
        start_index = 0
    else:
        start_index = (page - 1) * page_size

    end_index = start_index + page_size

    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                    i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        """
        assert isinstance(index, int) and 0 <= index < len(self.dataset())
        assert isinstance(page_size, int) and page_size > 0

        if index is None:
            index = 0

        start_index, end_index = index_range(index + 1, page_size)
        dataset = self.indexed_dataset()

        if start_index >= len(dataset):
            return {
                'index': index,
                'data': [],
                'page_size': page_size,
                'next_index': None
            }

        data = [dataset[i]
                for i in range(start_index, end_index) if i in dataset
                ]

        next_index = end_index if end_index < len(dataset) else None

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }
