#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
to expand the corpus to fit nltk tokenise
"""
import sqlite3
import os
import logging
import codecs


def split(inputFile, outFile):
    import nltk
    with codecs.open(inputFile, 'r', encoding='utf-8') as input:
        with codecs.open(outFile, 'w', encoding='utf-8') as output:
            for line in input:
                newData = ""
                words = line.strip().split('\t')
                if len(words)==1 and words[0]=='':
                    output.write('\r')
                    continue
                originalword = words[0]
                originaltag = words[1]
                newTokenizeWords = nltk.word_tokenize(originalword)

                if len(newTokenizeWords) == 1:
                    output.write("\t".join(words)+'\r')
                else:
                    newTokenizeWordTags = []
                    newTokenizeWordTags.append(words[1])
                    newTag = originaltag
                    if originaltag[0] == 'B':
                        newTag = originaltag.replace("B-", "I-", 1)

                    for i in range(1, len(newTokenizeWords)):
                        newTokenizeWordTags.append(newTag)
                    for i in range(len(newTokenizeWords)):
                        output.write(newTokenizeWords[i] + "\t" + newTokenizeWordTags[i]+'\r')


if __name__ == '__main__':
    split('train.conll','splittrain.conll')
