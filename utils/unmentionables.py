"""Utility generating unmentionables for a provided keyword.

Unmentionables currently consist of synset elements, hyponyms, and related
vector sums via word2vec.
"""
from nltk.corpus import wordnet as wn

__all__ = ('expand')

NUM_UNMENTIONABLES = 5

###################
# EXPOSED METHODS #
###################


def expand(word: str) -> set:
    """Expand a given word into a set of unmentionables.

    :param word: the keyword in taboo
    :param num: number of unmentionables to generate
    :return: set of 5 unmentionable words
    """
    words = set()
    add_hypernyms(word, words)
    add_hypernyms(word, words)
    return words


#########################
# ADDING UNMENTIONABLES #
#########################


def add_hypernyms(word: str, words: set) -> None:
    """Add hypernyms, more general terms.

    :param words: the set of words to amend
    """
    for synset in wn.synsets(word):
        for hypernym in synset.hypernyms():
            _add_all_lemmas(words, hypernym.lemmas())

# Support methods for adding unmentionables


def add_hyponyms(word: str, words: set) -> None:
    """Add hyponyms, more specific terms.

    :param words: the set of words to amend
    """
    for synset in wn.synsets(word):
        for hyponym in synset.hyponyms():
            _add_all_lemmas(hyponym.lemmas(), words)


def _add_all_lemmas(words: set, lemmas: list) -> None:
    """Add all lemmas to the provided set of words.

    :param lemmas: list of lemmas to add
    :param words: set of words to amend
    """
    for lemma in lemmas:
        _add_lemma(words, lemma)


def _add_lemma(words: set, lemma) -> None:
    """Add a lemma to the set of words."""
    if len(words) >= NUM_UNMENTIONABLES:
        return
    if filter_is_word(words, lemma) \
            and filter_same_roots(words, lemma):
        words.add(lemma.name())
        for antonym in lemma.antonyms():
            words.add(antonym.name())

############################
# FILTERING UNMENTIONABLES #
############################


def filter_is_word(words: set, lemma) -> bool:
    """Keep only words."""
    return _is_word(lemma)


def filter_same_roots(words: set, lemma) -> bool:
    """Keep only words that do not share the same root with existing words."""
    for word in words:
        if _have_same_root(word, lemma):
            return False
    return True


def _is_word(lemma) -> bool:
    """Check if a lemma_name is a single word, as opposed to a phrase."""
    return '_' not in lemma.name()


def _have_same_root(string1: str, string2: str) -> bool:
    """Check if two words share the same root."""
    return wn.morphy(string1) == wn.morphy(string2)
