#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
clean a large txt file,
generate two file,
the first one
"""
import codecs


def cleanCorpusFile(fileName, filteredPunctuationstFileName='SOwithoutPunctuations.txt',
                    filteredStopWordFileName='SOwithoutPunctuationsAndStopWord.txt'):
    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')

    english_stopwords.extend([word.capitalize() for word in english_stopwords])
    print english_stopwords
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']

    with codecs.open(fileName, encoding='utf-8') as file:
        with codecs.open(filteredPunctuationstFileName, 'w+', encoding='utf-8') as filteredPunctuationstFile:
            with codecs.open(filteredStopWordFileName, 'w+', encoding='utf-8') as filteredStopWordFile:
                for line in file:
                    words = line.strip('\n').split(' ')
                    texts_filtered_punctuations = [word for word in words if not word in english_punctuations]
                    texts_filtered_stopwords = [word for word in texts_filtered_punctuations if not word in english_stopwords]
                    filteredPunctuationstFile.write(" ".join(texts_filtered_punctuations)+" ")
                    filteredStopWordFile.write(" ".join(texts_filtered_stopwords)+" ")
if __name__ == '__main__':
    cleanCorpusFile('StackOverflowCorpus.txt')
