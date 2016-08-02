# Taboo

Taboo for web, iOS, and android with auto-generated cards

# Installation



# Command-Line Interface

The most general command is the first. Simply use

```
python taboo.py generate <path/to/source/file>
```

to generate an output file with a list of cleaned words and unmentionables.
The source file is a list of words, where each word has its own line.

```
Usage:
    taboo.py generate <src> [-v]
    taboo.py clean <src> [-v]
    taboo.py expand <word> [-v]
    taboo.py unmentionables <src> [-v]

Options:
    -h --help       Show this screen.
    -v --verbose   Print log messages and status updates
```
