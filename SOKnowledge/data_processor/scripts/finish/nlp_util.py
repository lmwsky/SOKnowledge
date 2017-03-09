#!/usr/bin/python
# -*- coding: utf-8 -*-

import fire
import nltk

from standford_nlp_wrapper import StanfordDocumentPreprocessor

REPLACE_CHAR_DIC = {
    '-LRB-': '(',
    '-RRB-': ')',
    '-LSB-': '[',
    '-RSB-': ']',
    '-LCB-': '{',
    '-RCB-': '}',
}


def word_tokenize_nltk(text):
    """
    parse a piece of text into word tokens,a wrap for nltk word_tokennize function
    :param text: the text need to splitted into tokens,ect."I am a person.And I am happy"
    :return: ['I', "am", 'a', 'person', '.', 'And', 'I', 'am', 'happy']
    """
    word_tokens = []
    if text:
        word_tokens = nltk.tokenize.word_tokenize(text)
    return word_tokens


def sent_tokenize_standford_nlp(text, tokenizer=None):
    """
    parse a piece of text into word tokens,a wrap for StanfordNLP word_tokennize function
    :param tokenizer: the tokenizer for text,tokenizer = StanfordDocumentPreprocessor()
    :param text: the text need to splitted into tokens,ect."I am a person.And I am happy."
    :return: ['I', "am", 'a', 'person', '.', 'And', 'I', 'am', 'happy','.']
    """
    sent_list = []

    if text:
        if tokenizer is None:
            tokenizer = StanfordDocumentPreprocessor()
        sent_list = tokenizer.tokenize(text)

    clean_text = "\n".join(sent_list)
    for old_char, new_char in REPLACE_CHAR_DIC.items():
        clean_text = clean_text.replace(old_char, new_char)
    return sent_tokenize_nltk(clean_text)


def sent_tokenize_nltk(text):
    """
    parse a piece of text into sentences,a wrap for nltk sent_tokenize function
    :param text: the text need to splitted into tokens,ect."I am a person.And I am happy."
    :return: ['I am a person.","And I am happy.']
    """
    sents = []
    if text:
        sents = nltk.tokenize.sent_tokenize(text)
    return sents


def sent_word_tokenize_nltk(text):
    """
    parse a piece of text into sentences,a wrap for nltk sent_tokenize function
    :param text: the text need to splitted into tokens,ect."I am a person.And I am happy."
    :return: ['I am a person.","And I am happy.']
    """
    sents = []
    if text:
        untokenize_sents = nltk.tokenize.sent_tokenize(text)
        for sent in untokenize_sents:
            sents.append(" ".join(nltk.tokenize.word_tokenize(sent)))
    return "\n".join(sents)


class DocumentPreProcessor(object):
    PUNCTUATION = ',.\'\\";:/?!'
    END_OF_SENTENCE_CHARS = '?.!'

    def __init__(self, reduce_whitespace=True, add_line_end_to_punctuation=True):
        self.preprocess_methods = []
        if reduce_whitespace:
            self.preprocess_methods.append(self._reduce_whitespace)
        if add_line_end_to_punctuation:
            self.preprocess_methods.append(self._add_line_end_to_punctuation)
        self.preprocess_methods.append(self.split_on_newline)

    def preprocess(self, document):
        for preprocess in self.preprocess_methods:
            document = preprocess(document)
        return document

    def _add_line_end_to_punctuation(self, document):
        processed_document = document.replace('\n', ' ')
        for eos in self.END_OF_SENTENCE_CHARS:
            processed_document = processed_document.replace(eos + ' ', eos + '\n')
        return processed_document

    def _reduce_whitespace(self, document):
        return nltk.re.sub("\s+", " ", document)

    def split_on_newline(self, document):
        return document.split('\n')


if __name__ == '__main__':
    fire.Fire(sent_word_tokenize_nltk)
