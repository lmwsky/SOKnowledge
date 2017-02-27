#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import nltk


def cleanSOText(htmlText):
    # the max code block size allowed save in text
    maxSingleCodeBlockSize = 30
    if htmlText is None or len(htmlText) == 0:
        return ["", [], []]
    soup = BeautifulSoup(htmlText, "lxml")
    codeBlocksNum = 1
    codeBlocks = []
    codeBlocksNames = []
    tokenizeText = ""
    codeTags = soup.find_all(name="code")
    for tag in codeTags:
        if tag.parent.name == "pre":
            if tag.string and (len(tag.string) > maxSingleCodeBlockSize or tag.string.find(" ") != -1):
                name = "@code" + str(codeBlocksNum) + "@"
                codeBlocks.append(tag.string)
                codeBlocksNames.append(name)
                tag.string = name
                codeBlocksNum += 1

    cleanText=soup.get_text()
    sents=nltk.sent_tokenize(cleanText)

    wordsText=[]
    for s in sents:
        words=nltk.word_tokenize(s)
        wordsText.append(" ".join(words))
    tokenizeText="\n".join(wordsText)

    return [cleanText, codeBlocksNames, codeBlocks, tokenizeText]


if __name__ == '__main__':
    testText = """
<p>I want my intent to be launched when the user goes to a certain url: for example, the android market does this with <a href="http://market.android.com/">http://market.android.com/</a> urls. so does youtube. I want mine to do that too.</p>
"""
    [text, codeBlocksNames,codeBlocks, tokenizeText] = cleanSOText(testText)
    print(text)
    print (codeBlocksNames)
    print (codeBlocks)
    print (tokenizeText)
