#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
import logging

from cleanSOTextUtil import cleanSOText

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


def cleanPostsBody(file_names, anathomy,
                   dump_path='.',
                   dump_database_name='so-dump.db',
                   create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
                   insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
                   select_query="SELECT Id, Body FROM posts WHERE Id>{minRow} AND Id<= {maxRow}",
                   log_filename='so-parser.log',
                   startId=0,
                   endId=34573264,
                   step=10000
                   ):
    insertCodeBlockQuery = insert_query.format(
        table='codeBlock',
        columns=', '.join(['ParentId', 'Name', 'BlockText']),
        values=('?, ' * len(anathomy['codeBlock'].keys()))[:-2])
    insertPostsTextQuery = insert_query.format(
        table='postsText',
        columns=', '.join(['PostId', 'Content']),
        values=('?, ' * 2)[:-2])
    insertTokenizeTextQuery= insert_query.format(
        table='tokenizePostsText',
        columns=', '.join(['PostId', 'TokenizeContent']),
        values=('?, ' * 2)[:-2])
    logging.basicConfig(filename=os.path.join(dump_path, log_filename), level=logging.INFO)
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    # create Table
    for file in file_names:
        table_name = file
        sql_create = create_query.format(
            table=table_name,
            fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
        print('Creating table {0}'.format(table_name))

        try:
            logging.info(sql_create)
            db.execute(sql_create)
        except Exception, e:
            logging.warning(e)

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
            Id = row[0]
            Body = row[1]
            if Body is None or Body == "":
                continue
            [text, codeBlockNames, codeBlocks,tokenizeText] = cleanSOText(Body)
            try:
                db.execute(insertPostsTextQuery, [Id, text])
                db.execute(insertTokenizeTextQuery, [Id, tokenizeText])
                if codeBlockNames:
                    for index in range(len(codeBlockNames)):
                        db.execute(insertCodeBlockQuery, [Id, codeBlockNames[index], codeBlocks[index]])
            except Exception, error:
                print error
        cursor.close()

        s += step
        e = min(s + step, endId)
    db.commit()


if __name__ == '__main__':
    cleanPostsBody(ANATHOMY.keys(), ANATHOMY, step=100, endId=720)
