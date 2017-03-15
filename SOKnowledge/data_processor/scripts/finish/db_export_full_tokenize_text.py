#!/usr/bin/python
# -*- coding: utf-8 -*-

import fire

from anatomy import CODE_BLOCK_TYPE, CODE_BLOCK_QUERY_TYPE
from db_util import build_connect_to_sqlite_with_row_factory
from sql_util import get_query_code_block_sql


def query_code_block_dict(parent_id,
                          code_block_table_name,
                          code_block_type=CODE_BLOCK_TYPE.ALL,
                          db_connection=None,
                          dump_path='.',
                          dump_database_name='so-dump.db'):
    is_new_connection = False
    cursor = None
    try:
        if db_connection is None:
            is_new_connection = True
            db_connection = build_connect_to_sqlite_with_row_factory(db_connection, dump_database_name, dump_path)
        cursor = db_connection.cursor()

        sql = get_query_code_block_sql(code_block_table_name, parent_id, code_block_type)

        cursor = cursor.execute(sql)
        code_block_dict = {}
        for row in cursor.fetchall():
            code_block_name = row['codeBlockName']
            code_block_dict[code_block_name] = row['codeBlock']
        return code_block_dict
    except Exception, e:
        print e
    finally:
        if is_new_connection:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()


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


def get_post_text(post_id,
                  post_text_table_name,
                  post_text_col_name,
                  code_block_table_name,
                  code_block_select_mode=CODE_BLOCK_QUERY_TYPE.FULL,
                  post_text_table_primary_key_name="Id",
                  db_connection=None,
                  dump_path='.',
                  dump_database_name='so-dump.db'):
    post_body_text, code_block_dict = get_post_no_code_body_text_and_code_block(post_id,
                                                                                post_text_table_name,
                                                                                post_text_col_name,
                                                                                code_block_table_name,
                                                                                code_block_select_mode,
                                                                                post_text_table_primary_key_name,
                                                                                db_connection,
                                                                                dump_path,
                                                                                dump_database_name)
    return join_code_block_into_text(post_body_text, code_block_dict)


def get_post_no_code_body_text_and_code_block(post_id,
                                              post_text_table_name,
                                              post_text_col_name,
                                              code_block_table_name,
                                              code_block_select_mode=CODE_BLOCK_QUERY_TYPE.FULL,
                                              post_text_table_primary_key_name="Id",
                                              db_connection=None,
                                              dump_path='.',
                                              dump_database_name='so-dump.db',
                                              ):
    post_body_text = get_one_row_col_value_from_db(post_text_table_name, post_text_table_primary_key_name, post_id,
                                                   post_text_col_name, db_connection, dump_path, dump_database_name)

    if code_block_select_mode == CODE_BLOCK_QUERY_TYPE.NONE:
        return post_body_text, {}
    if code_block_select_mode == CODE_BLOCK_QUERY_TYPE.HALF:
        from db_remove_tag import CODE_BLOCK_TYPE_SMALL
        code_block_dict = query_code_block_dict(post_id,
                                                code_block_table_name,
                                                CODE_BLOCK_TYPE_SMALL,
                                                db_connection,
                                                dump_path,
                                                dump_database_name)
        return post_body_text, code_block_dict

    if code_block_select_mode == CODE_BLOCK_QUERY_TYPE.FULL:
        code_block_dict = query_code_block_dict(post_id,
                                                code_block_table_name,
                                                CODE_BLOCK_TYPE.ALL,
                                                db_connection,
                                                dump_path,
                                                dump_database_name)
        return post_body_text, code_block_dict


def get_one_row_col_value_from_db(
        table_name,
        primary_key_name,
        primary_key_value,
        col_name,
        db_connection=None,
        dump_path='.',
        dump_database_name='so-dump.db'):
    is_new_connection = False
    cursor = None
    try:
        if db_connection is None:
            is_new_connection = True
            db_connection = build_connect_to_sqlite_with_row_factory(dump_database_name, dump_path)
        select_query = 'SELECT * FROM {table} WHERE {primary_key_name}={primary_key_value}'
        select_sql = select_query.format(table=table_name,
                                         primary_key_name=primary_key_name, primary_key_value=primary_key_value)
        print select_sql
        cursor = db_connection.cursor()
        cursor = cursor.execute(select_sql)
        row = cursor.fetchone()

        if row:
            return row[col_name]
        else:
            return None

    except Exception, error:
        print error
    finally:
        if is_new_connection:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()


if __name__ == '__main__':
    fire.Fire(query_code_block_dict)
