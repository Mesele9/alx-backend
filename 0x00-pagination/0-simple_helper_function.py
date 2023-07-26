#!/usr/bin/env python3
""" 0-simpler_helper_function.py """


def index_range(page, page_size):
    """ a function that takes two integer arguments page and page_size, and
    return a tuple of size two containing a start index and an end index. """
    if page <= 1:
        start_index = 0
    else:
        start_index = (page - 1) * page_size
        
    end_index = start_index + page_size

    return start_index, end_index
