#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
a script to export the clean text of SO from sqlite into one txt file as corpus
this file will be used to train word vector for google word2vec tool
"""
import sqlite3
import os
import logging
import codecs

ANATHOMY = {
    'codeBlock': {
        'ParentId': 'INTEGER',
        'Name': 'TEXT',
        'BlockText': 'TEXT'
    },
    'postsText': {
        'PostId': 'INTEGER',
        'Content': 'TEXT'
    },
    'tokenizePostsText': {
        'PostId': 'INTEGER',
        'TokenizeContent': 'TEXT'
    }
}


def export(fileName,
                   dump_path='.',
                   dump_database_name='so-dump.db',
                   select_query="SELECT TokenizeContent FROM tokenizePostsText WHERE PostId>{minRow} AND PostId<= {maxRow}",
                   startId=0,
                   endId=34573264,
                   step=10000
                   ):
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))

    exportFile=codecs.open(fileName,"w","utf-8")
    s = startId
    e = min(startId + step, endId)
    while s < endId:
        try:
            query = select_query.format(minRow=s, maxRow=e)
            cursor = db.execute(query)
        except Exception, error:
            logging.warning(error)
            print error

        for row in cursor:
            TokenizeContent = row[0]
            if TokenizeContent is None or TokenizeContent == "":
                continue
            exportFile.write(TokenizeContent)
        cursor.close()

        s += step
        e = min(s + step, endId)

    exportFile.close()

if __name__ == '__main__':
    export('SOTestForNER.txt',endId=2000)