"""
a script to export the clean text of SO from sqlite into one txt file as corpus
this file will be used to train word vector for google word2vec tool
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import multiprocessing

import fire
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def train_word_embedding(corpus_file_path='.', corpus_file_name='corpus.txt', model_name='so_word_embedding_model',
                         binary_model_file_name='word_embedding.bin', not_binary_model_file_name='word_embedding.txt'):
    model = Word2Vec(LineSentence(os.path.join(corpus_file_path, corpus_file_name)), size=400, window=5, min_count=10,
                     workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use(much) less RAM
    # model.init_sims(replace=True)
    model.save(os.path.join(corpus_file_path, model_name))
    model.wv.save_word2vec_format(os.path.join(corpus_file_path, binary_model_file_name), binary=True)
    model.wv.save_word2vec_format(os.path.join(corpus_file_path, not_binary_model_file_name), binary=False)


if __name__ == '__main__':
    fire.Fire(train_word_embedding)
