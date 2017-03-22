import codecs
import os
from unittest import TestCase

from annotator.data_set_util import build_conll_fomat_for_sentence


class TestBuild_conll_fomat_for_sentence(TestCase):
    def test_build_conll_fomat_for_sentence(self):
        text = build_conll_fomat_for_sentence(['we', 'are', 'young'], ['O', 'O', 'O'])
        with codecs.open(os.path.join('.','testo.txt'), 'a', encoding='utf-8') as out:
            out.write(text)

