"""Command-line interface for the Taboo utility.

This utility includes generation scripts and related subprocesses.

Usage:
    taboo.py generate <src> [options]
    taboo.py clean <src> [options]
    taboo.py expand <word> [options]
    taboo.py unmentionables <src> [options]
    taboo.py scrape (--noswearing | --dictionary) [--force] [options]
    taboo.py tojs <src>

Options:
    -h --help       Show this screen.
    -v --verbose   Print log messages and status updates
"""

from constants import CLEANED_FILE_NAME
from constants import JS_FILE_NAME
from constants import OUTPUT_FILE_NAME
from docopt import docopt
from utils.clean import clean
from utils.unmentionables import expand
from utils.scraper import scrape
from utils.scraper import read_lines


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
    elif arguments['scrape']:
        _scrape(arguments)
    elif arguments['tojs']:
        _tojs(
            src=arguments['<src>'],
            dest=JS_FILE_NAME,
            verbose=arguments['--verbose'])


def _clean(src: str, dest: str, verbose: bool) -> None:
    """Clean the provided file and output to file.

    :param from: the source file to read from
    :param to: the target file to write to
    :param verbose: whether or not to print statuses
    """
    with open(dest, 'w') as f:
        for i, w in enumerate(clean(set(read_lines(src)))):
            f.write(w + '\n')
    print(i + 1, 'words written to', dest)


def _unmentionables(src: str, dest: str, verbose: bool) -> None:
    """Generate unmentionables for the provided file of words.

    Prints the total number of words written, and in verbose mode, prints a
    status for each word written.

    :param from: the source file to read from
    :param to: the target file to write to
    :param verbose: whether or not print statuses
    """
    with open(dest, 'w') as f:
        for n, w in enumerate(read_lines(src)):
            expanded_set = expand(w)
            if verbose:
                print('Word {n}: {word} ({num_words})'.format(
                    n=n,
                    word=w,
                    num_words=len(expanded_set)))
            f.write('{word} | {unmentionables}\n'.format(
                word=w,
                unmentionables=' '.join(expanded_set)))
    print(n + 1, 'words written to', dest)


def _scrape(arguments: dict):
    """Scrape the provided target.

    :param target: the name of the scraper to invoke
    """
    verbose = arguments['--verbose']
    force = arguments['--force']
    if arguments['--noswearing']:
        scrape('noswearing', verbose, force)

def _tojs(src: str, dest: str, verbose: bool) -> None:
    """Generate javascript file with list from output.

    Specifically, creates a list of pairs, with (word, unmentionables).

    :param from: the source file to read from
    :param to: the target file to write to
    :param verbose: whether or not print statuses
    """
    with open(dest, 'w') as f:
        f.write('words = [\n')
        for line in read_lines(src):
            keyword, unmentionables = line.split('|')
            new_line = '["{keyword}", ["{unmentionables}"]],\n'.format(
                keyword=keyword.strip(),
                unmentionables='","'.join(unmentionables.strip().split(' ')))
            f.write(new_line)
        f.write('];')

if __name__ == '__main__':
    main(docopt(__doc__, version='Taboo 1.0'))
