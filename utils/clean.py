"""Cleaning utility for list of words.

This module includes utilities for stripping out articles and other
non-taboo-worthy words.
"""
from nltk.corpus import stopwords
from utils.scraper import read_lines
from constants import SWEARWORDS_FILE_NAME

__all__ = ('clean')


def clean(words: set) -> set:
    """Accept a set of words and prune unworthy words.

    :param words: set of words to clean
    :return: filtered set of words
    """
    blacklist = stopwords.words('english')
    blacklist.extend(read_lines(SWEARWORDS_FILE_NAME))
    return {w for w in words if w not in blacklist and len(w) > 2}
