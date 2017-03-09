#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3

import fire


def query_code_block_dict(id,
                          code_block_table_name,
                          db_connection=None,
                          dump_path='.',
                          dump_database_name='so-dump.db',
                          select_query="SELECT * FROM {table} where ParentId={id}"):
    try:
        if db_connection is None:
            dump_full_path = os.path.join(dump_path, dump_database_name)
            db_connection = sqlite3.connect(dump_full_path)
            db_connection.row_factory = sqlite3.Row
        cursor = db_connection.cursor()
        sql = select_query.format(table=code_block_table_name, id=id)
        cursor = cursor.execute(sql)
        print sql
        code_block_dict = {}
        for row in cursor.fetchall():
            codeBlockName = row['codeBlockName']
            code_block_dict[codeBlockName] = row['codeBlock']
        cursor.close()
        db_connection.close()
        return code_block_dict
    except Exception, e:
        print e


def join_code_block_into_text(text, code_block_dict=None):
    """
    replace the code name tag in text to the correspond code block
    :param text:the text contain code blcok name,ect,"_lc1_","_sc2"
    :param code_block_dict:the code name and code block dict
    :return:the joint text
    """
    if code_block_dict is None:
        code_block_dict = {}
    if text:
        for code_block_name, code_block in code_block_dict.items():
            text = text.replace(code_block_name, code_block)
    else:
        return ""


def testFile():
    return {"f": 1}


if __name__ == '__main__':
    fire.Fire(query_code_block_dict)
