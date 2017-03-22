import codecs
import os
from unittest import TestCase

from annotator.data_set_util import build_conll_fomat_for_sentences


class TestBuild_conll_fomat_for_sentences(TestCase):
    def test_build_conll_fomat_for_sentences(self):
        text = build_conll_fomat_for_sentences([['we', 'are', 'young', '.'], ['I', 'am', 'happy', '.']],
                                               [['O', 'O', 'O', 'O'], ['B-PERSON', 'O', 'O', 'O']])
        with codecs.open(os.path.join('.', 'testo.txt'), 'W', encoding='utf-8') as out:
            out.write(text)
