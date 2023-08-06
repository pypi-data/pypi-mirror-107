from difflib import get_close_matches
from typing import AnyStr, List

def autocorrect(word: AnyStr, words: List[AnyStr], *args, **kwargs):
    globbed = get_close_matches(word, words, 1, *args, **kwargs) or word
    if isinstance(globbed, list):
        globbed = globbed[0]
    assert isinstance(globbed, str)
    return globbed
