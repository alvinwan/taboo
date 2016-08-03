# Taboo Command-Line Interface

The command-line interface handles selection of words and related
unmentionables for the game taboo.

# Usage

The most general command is the first. Simply use

```
python taboo.py generate <path/to/source/file>
```

to generate an output file with a list of cleaned words and unmentionables.
The source file is a list of words, where each word has its own line.

```
Usage:
    taboo.py generate <src> [options]
    taboo.py clean <src> [options]
    taboo.py expand <word> [options]
    taboo.py unmentionables <src> [options]
    taboo.py scrape (--noswearing | --dictionary) [--force] [options]

Options:
    -h --help       Show this screen.
    -v --verbose   Print log messages and status updates
```

# Installation

## Python Virtual Environment

It is highly recommended that you start a virtual environment for python.

### Using Anaconda

With Anaconda,

```
conda create -n taboo python=3.5
```

Then, to start your virtual environment:

```
source activate taboo
```

### Using Python's Built-in

If you do not have Anaconda installed, you can also use the following

```
python3.5 -m venv env
```

Then, to start your virtual environment:

```
source env/bin/activate
```

## Python Dependencies

Once in your virtual environment, run the following to install all Python
dependencies required for this project.

```
pip install -r requirements.txt
```
