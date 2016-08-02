"""Utility generating unmentionables for a provided keyword.

Unmentionables currently consist of synset elements, hyponyms, and related
vector sums via word2vec.
"""
from nltk.corpus import wordnet as wn

__all__ = ('expand')


def expand(word: str) -> set:
    """Expand a given word into a set of unmentionables.

    :param word: the keyword in taboo
    :return: set of 5 unmentionable words
    """
    words = set()
    for synset in wn.synsets(word):
        if len(words) >= 5:
            break
        words |= {
            lemma.name() for lemma in synset.lemmas()
            if lemma.name() != word and _is_word(lemma)}
    return set(list(words)[:5])  # inefficient

def _is_word(lemma) -> bool:
    """Check if a lemma is a single word, as opposed to a phrase."""
    return '_' not in lemma.name()
