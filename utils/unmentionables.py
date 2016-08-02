"""Utility generating unmentionables for a provided keyword.

Unmentionables currently consist of synset elements, hyponyms, and related
vector sums via word2vec.
"""
from nltk.corpus import wordnet as wn

__all__ = ('expand')

DEFAULT_NUM_UNMENTIONABLES = 5


def expand(word: str, num: int=DEFAULT_NUM_UNMENTIONABLES) -> set:
    """Expand a given word into a set of unmentionables.

    :param word: the keyword in taboo
    :param num: number of unmentionables to generate
    :return: set of 5 unmentionable words
    """
    words = set()
    for synset in wn.synsets(word):
        if len(words) >= num:
            break
        for hypernym in synset.hypernyms():
            _add_all_lemmas(hypernym.lemmas(), words)
        for hyponym in synset.hyponyms():
            _add_all_lemmas(hyponym.lemmas(), words)
    return set(list(words)[:num])  # inefficient


def have_same_root(string1: str, string2: str) -> bool:
    """Check if two words share the same root"""
    return wn.morphy(string1) == wn.morphy(string2)


def _add_all_lemmas(lemmas: list, words: set) -> None:
    """Add all lemmas to the provided set of words.

    :param lemmas: list of lemmas to add
    :param words: set of words to amend
    """
    for lemma in lemmas:
        if _is_word(lemma):
            words.add(lemma.name())
            for antonym in lemma.antonyms():
                words.add(antonym.name())


def _is_word(lemma) -> bool:
    """Check if a lemma_name is a single word, as opposed to a phrase."""
    return '_' not in lemma.name()
