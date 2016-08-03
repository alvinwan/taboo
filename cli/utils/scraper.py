"""Scrapers available for the Taboo utility."""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from http.client import RemoteDisconnected
from constants import NO_SWEARING_URL_BY_LETTER
from constants import NO_SWEARING_CACHED_FILENAME

import string
import os


__all__ = ('scrape', 'scrape_noswearing', 'read_lines')


def scrape(target: str, verbose: bool, force: bool=False) -> [str]:
    """Exposed scraping utility that invokes associated modules.

    :param target: name of target scraper
    :param verbose: whether or not to print statuses
    :param force: if true, cached file results will not be used
    :return: list of string results
    """
    if target == 'noswearing':
        scrape_noswearing(verbose, force)


def scrape_noswearing(verbose: bool, force: bool) -> [str]:
    """Scrape noswearing.com for swear words."""
    words = list()
    for letter in string.ascii_lowercase:
        new_words = _get_words(letter, verbose, force)
        _save_to_file(letter, new_words)
        words.extend(new_words)
    _save_to_file('all', words)
    return words


def read_lines(f):
    """Convert a file into a list of strings, without line breaks."""
    return [line.strip() for line in open(f)]


def _get_words(letter: str, verbose: bool, force: bool) -> [str]:
    """Open the cached results or access the website."""
    words = _read_from_file(letter, verbose)
    if words and not force:
        return words
    return _read_from_url(letter, verbose)


def _read_from_url(letter: str, verbose: bool) -> [str]:
    """Read words from the web."""
    if verbose:
        print('Scraping', letter, '...')
    soup = BeautifulSoup(_url_open(letter, verbose), 'html.parser')
    return [
        e.string for e in soup.find_all('table')[2].find_all('b')
        if e.string != 'More Slang Translators:']


def _url_open(letter: str, verbose: bool) -> str:
    """Open URL for the provided letter, and try until success."""
    try:
        contents = urlopen(NO_SWEARING_URL_BY_LETTER.format(letter=letter))
    except RemoteDisconnected:
        if verbose:
            print('Retrying', letter, '...')
        return _url_open(letter, verbose)
    return contents


def _read_from_file(letter: str, verbose: bool) -> [str]:
    """Attempts to read from the cached file associated with provided letter.

    The file will be read if it exists and return the contents of the file.
    Otherwise, it will return None.
    """
    filename = NO_SWEARING_CACHED_FILENAME.format(letter=letter)
    if os.path.isfile(filename):
        if verbose:
            print(filename, 'found')
        return read_lines(filename)
    return None


def _save_to_file(letter: str, words: list) -> None:
    """Write all words to the cached file assoc. with the provided letter."""
    filename = NO_SWEARING_CACHED_FILENAME.format(letter=letter)
    with open(filename, 'w') as f:
        for word in words:
            f.write(word + '\n')
