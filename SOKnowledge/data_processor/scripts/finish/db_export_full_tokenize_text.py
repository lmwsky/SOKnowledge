#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3

import fire


def generate_select_code_block_sql(code_block_table_name, parent_id, type=None):
    if type:
        return "SELECT * FROM {table} where ParentId={id} AND type={type}".format(table=code_block_table_name,
                                                                                  id=parent_id, type=type)
    else:
        return "SELECT * FROM {table} where ParentId={id}".format(table=code_block_table_name,
                                                                  id=parent_id)


def query_code_block_dict(parent_id,
                          code_block_table_name,
                          type=None,
                          dump_path='.',
                          dump_database_name='so-dump.db',
                          db_connection=None,
                          ):
    is_create_db_connection = False
    cursor = None
    try:
        if db_connection is None:
            dump_full_path = os.path.join(dump_path, dump_database_name)
            db_connection = sqlite3.connect(dump_full_path)
            db_connection.row_factory = sqlite3.Row
            is_create_db_connection = True
        cursor = db_connection.cursor()
        sql = generate_select_code_block_sql(code_block_table_name, parent_id, type)
        cursor = cursor.execute(sql)
        code_block_dict = {}
        for row in cursor.fetchall():
            codeBlockName = row['codeBlockName']
            code_block_dict[codeBlockName] = row['codeBlock']
        return code_block_dict
    except Exception, e:
        print e
    finally:
        if cursor:
            cursor.close()
        if is_create_db_connection:
            db_connection.close()

def row_join_code_block_into_text(
                                 ):
    pass

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
