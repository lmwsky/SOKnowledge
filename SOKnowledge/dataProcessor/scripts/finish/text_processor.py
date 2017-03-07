#!/usr/bin/python
# -*- coding: utf-8 -*-
import fire
from bs4 import BeautifulSoup


def remove_tags(html_text):
    """
    delete all tags in html text(except code tag,all codeBlock is replace with string,
    '_lc[1-9][0-9]*_' or '_sc[1-9][0-9]*_' is a regular expression which can match codeBlock name string),
    'l'--large stands for the <code><code> contents are large,and the <code> tags are wrapped in <pre> tag,
    's' --small stands for the <code><code> contents are small,and the <code> tags are not wrapped in <pre> tag,
    return the clean text,and codeBlock names and codeBlock
    :param html_text:a piece of  html text with a lot of tags
    :return: a dict,has three  keys,'cleanText',
            cleanText -- all tags removed,but replace the <code><code> element with codeBlocksNames,
            largeCodeDict -- all the replaced long codeBlock names as key,etc.'@lc1@',and value is the original text
            smallCodeDict -- all the replaced small codeBlock names as key,etc.'@sc1@',and value is the original text

    """

    soup = BeautifulSoup(html_text, "lxml")
    codeTags = soup.find_all(name="code")

    cleanText = ""

    largeCodeDict = {}
    smallCodeDict = {}

    largeCodeBlocksNum = 1
    smallCodeBlocksNum = 1

    if html_text is not None and len(html_text) > 0:
        for tag in codeTags:
            if tag.string:
                if tag.parent.name == "pre":
                    name = "_lc" + str(largeCodeBlocksNum) + "_"
                    largeCodeDict[name] = tag.string
                    tag.string = name
                    largeCodeBlocksNum += 1
                else:
                    name = "_sc" + str(smallCodeBlocksNum) + "_"
                    smallCodeDict[name] = tag.string
                    tag.string = name
                    smallCodeBlocksNum += 1

        cleanText = soup.get_text()

    result = {}
    result['cleanText'] = cleanText
    result['largeCodeDict'] = largeCodeDict
    result['smallCodeDict'] = smallCodeDict
    return result


if __name__ == '__main__':
    fire.Fire(remove_tags)
