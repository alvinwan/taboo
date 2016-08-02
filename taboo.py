"""CLI for the taboo utility.

Usage:
    taboo.py generate <src> [-v]
    taboo.py clean <src> [-v]
    taboo.py expand <word> [-v]
    taboo.py unmentionables <src> [-v]

Options:
    -h --help       Show this screen.
    -v --verbose   Print log messages and status updates
"""

from utils.clean import clean
from utils.unmentionables import expand, NUM_UNMENTIONABLES
from docopt import docopt

import os

TARGET_DIR = 'out'
CLEANED_FILE_NAME = os.path.join(TARGET_DIR, 'cleaned.txt')
OUTPUT_FILE_NAME = os.path.join(TARGET_DIR, 'output.txt')


def main(arguments: dict):
    """Main function, processes commands and invokes relevant modules.

    :param arguments: dictionary of all CLI arguments
    """
    if arguments['generate']:
        _clean(
            src=arguments['<src>'],
            dest=CLEANED_FILE_NAME,
            verbose=arguments['--verbose'])
        _unmentionables(
            src=CLEANED_FILE_NAME,
            dest=OUTPUT_FILE_NAME,
            verbose=arguments['--verbose'])
    elif arguments['expand']:
        print(expand(arguments['<word>']))
    elif arguments['clean']:
        _clean(
            src=arguments['<src>'],
            dest=CLEANED_FILE_NAME,
            verbose=arguments['--verbose'])
    elif arguments['unmentionables']:
        _unmentionables(
            src=arguments['<src>'],
            dest=OUTPUT_FILE_NAME,
            verbose=arguments['--verbose'])


def _clean(src: str, dest: str, verbose: bool) -> None:
    """Clean the provided file and output to file.

    :param from: the source file to read from
    :param to: the target file to write to
    """
    words_written = 0
    with open(dest, 'w') as f:
        for w in clean(_read_lines(src)):
            words_written += 1
            f.write(w + '\n')
    print(words_written, 'words written to', dest)


def _unmentionables(src: str, dest: str, verbose: bool) -> None:
    """Generate unmentionables for the provided file of words.

    :param from: the source file to read from
    :param to: the target file to write to
    """
    words_written = 0
    with open(dest, 'w') as f:
        for n, w in enumerate(_read_lines(src)):
            if verbose:
                print('Word {n}: {word}'.format(n=n, word=w))
            expanded_set = expand(w)
            words_written += 1
            f.write('{word} | {unmentionables}\n'.format(
                word=w,
                unmentionables=' '.join(expanded_set)))
    print(words_written, 'words written to', dest)


def _read_lines(f):
    return {line.strip() for line in open(f)}


if __name__ == '__main__':
    main(docopt(__doc__, version='Taboo 1.0'))
