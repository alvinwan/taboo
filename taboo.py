"""CLI for the taboo utility.

Usage:
taboo.py clean <from>
"""

from utils.clean import clean
from docopt import docopt


CLEANED_DATA_SOURCE = 'data/cleaned.txt'


def main(arguments: dict):
    """Main function, processes commands and issues data to relevant modules."""
    if arguments['clean']:
        with open(CLEANED_DATA_SOURCE, 'w') as f:
            for w in clean({w.strip() for w in open(arguments['<from>'])}):
                f.write(w + '\n')


if __name__ == '__main__':
    main(docopt(__doc__, version='Taboo'))
