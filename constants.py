"""Constants for Taboo utility."""

import os


SOURCE_DIR = 'data'
TARGET_DIR = 'out'
CLEANED_FILE_NAME = os.path.join(TARGET_DIR, 'cleaned.txt')
OUTPUT_FILE_NAME = os.path.join(TARGET_DIR, 'output.txt')

"""
:param letter: curse words beginning with this letter
"""
NO_SWEARING_URL_BY_LETTER = 'http://www.noswearing.com/dictionary/{letter}'

"""
:param letter: curse words beginning with this letter
"""
NO_SWEARING_CACHED_FILENAME = os.path.join(SOURCE_DIR, 'swearing-{letter}.txt')

SWEARWORDS_FILE_NAME = NO_SWEARING_CACHED_FILENAME.format(letter='all')
