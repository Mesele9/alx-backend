#!/usr/bin/env python3
""" 1-simpler_helper_function.py """
import csv
import math
from typing import List


def index_range(page, page_size):
    """ a function that takes two integer arguments page and page_size, and
    return a tuple of size two containing a start index and an end index.
    """
    if not isinstance(page, int) or not isinstance(page_size, int)
    or page <= 0:
        raise AssertionError("Both page and page_size should be
                             positive integers.")

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index


class Server:
    """ Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """a method that takes two integer arguments page and page_size and
        Use index_range to find the correct indexes to paginate the dataset
        correctly and return the appropriate page of the dataset
        (i.e. the correct list of rows).
        """
        try:
            start_index, end_index = index_range(page, page_size)
        except AssertionError:
            return []

        dataset = self.dataset()
        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
