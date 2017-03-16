#!/usr/bin/python
# -*- coding: utf-8 -*-

import fire

from anatomy import CODE_BLOCK_TYPE, CODE_BLOCK_QUERY_TYPE, TABLE_NAMES
from db_util import build_connect_to_sqlite_with_row_factory
from sql_util import get_query_code_block_sql, generate_select_question_id_list


def query_code_block_dict(parent_id,
                          code_block_table_name=TABLE_NAMES.CODE_BLOCK_WITH_TOKENIZE_CODE,
                          code_block_type=CODE_BLOCK_TYPE.ALL,
                          code_block_text_col_name="tokenize_text",
                          db_connection=None,
                          dump_path='.',
                          dump_database_name='so-dump.db'):
    is_new_connection = False
    cursor = None
    try:
        if db_connection is None:
            is_new_connection = True
            db_connection = build_connect_to_sqlite_with_row_factory(dump_path, dump_database_name)
        cursor = db_connection.cursor()

        sql = get_query_code_block_sql(code_block_table_name, parent_id, code_block_type)

        cursor = cursor.execute(sql)
        code_block_dict = {}
        for row in cursor.fetchall():
            code_block_name = row['codeBlockName']
            code_block_dict[code_block_name] = row[code_block_text_col_name]
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
        return text
    else:
        return ""


def get_post_text(post_id,
                  post_text_table_name=TABLE_NAMES.TOKENIZE_REMOVE_TAG_POSTS_BODY,
                  post_text_col_name="tokenize_text",
                  code_block_table_name=TABLE_NAMES.CODE_BLOCK_WITH_TOKENIZE_CODE,
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
                                              post_text_table_name=TABLE_NAMES.TOKENIZE_REMOVE_TAG_POSTS_BODY,
                                              post_text_col_name="tokenize_text",
                                              code_block_table_name=TABLE_NAMES.CODE_BLOCK_WITH_TOKENIZE_CODE,
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
        code_block_dict = query_code_block_dict(post_id,
                                                code_block_table_name,
                                                CODE_BLOCK_TYPE.SMALL,
                                                db_connection=db_connection,
                                                dump_path=dump_path,
                                                dump_database_name=dump_database_name)
        return post_body_text, code_block_dict

    if code_block_select_mode == CODE_BLOCK_QUERY_TYPE.FULL:
        code_block_dict = query_code_block_dict(post_id,
                                                code_block_table_name,
                                                CODE_BLOCK_TYPE.ALL,
                                                db_connection=db_connection,
                                                dump_path=dump_path,
                                                dump_database_name=dump_database_name)
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
            db_connection = build_connect_to_sqlite_with_row_factory(dump_path, dump_database_name)
        select_query = 'SELECT * FROM {table} WHERE {primary_key_name}={primary_key_value}'
        select_sql = select_query.format(table=table_name,
                                         primary_key_name=primary_key_name, primary_key_value=primary_key_value)
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


def get_question_all_answer_id_list(
        question_id,
        db_connection=None,
        dump_path=".",
        dump_database_name='so-dump.db',
):
    is_create_connection = False
    cursor = None
    if db_connection is None:
        is_create_connection = True
        db_connection = build_connect_to_sqlite_with_row_factory(dump_path, dump_database_name)
    try:
        select_query = "SELECT Id FROM {table} WHERE ParentId={question_id}"
        table_name = TABLE_NAMES.POSTS

        id_list = []
        cursor = db_connection.cursor()
        sql = select_query.format(table=table_name, question_id=question_id)
        cursor = cursor.execute(sql)
        for row in cursor.fetchall():
            id_list.append(row["Id"])
        return id_list
    except Exception, e:
        print e
    finally:
        if is_create_connection:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()


def get_question_and_answers(question_id,
                             code_block_exist_type=CODE_BLOCK_QUERY_TYPE.HALF,
                             db_connection=None,
                             dump_path=".",
                             dump_database_name='so-dump.db', ):
    question_text = get_post_text(post_id=question_id,
                                  code_block_select_mode=code_block_exist_type,
                                  db_connection=db_connection,
                                  dump_path=dump_path,
                                  dump_database_name=dump_database_name)
    answer_text_list = get_all_answer_text(question_id=question_id,
                                           code_block_exist_type=code_block_exist_type,
                                           db_connection=db_connection,
                                           dump_path=dump_path,
                                           dump_database_name=dump_database_name)
    return question_text, answer_text_list


def get_all_answer_text(
        question_id,
        code_block_exist_type=CODE_BLOCK_QUERY_TYPE.HALF,
        db_connection=None,
        dump_path=".",
        dump_database_name='so-dump.db',
):
    answer_id_list = get_question_all_answer_id_list(question_id, db_connection=db_connection,
                                                     dump_database_name=dump_database_name, dump_path=dump_path)
    answer_text_list = []
    if answer_id_list:
        for id in answer_id_list:
            answer_text = get_post_text(post_id=id,
                                        code_block_select_mode=code_block_exist_type,
                                        db_connection=db_connection,
                                        dump_path=dump_path,
                                        dump_database_name=dump_database_name)
            if answer_text:
                answer_text_list.append(answer_text)
    return answer_text_list


def cursor_process_simple_return_id_list(cursor):
    id_list = []
    for row in cursor.fetchall():
        id = row["Id"]
        id_list.append(id)
    return id_list


def process_question_id_list(
        min_id=None,
        max_id=None,
        cursor_processor_func=cursor_process_simple_return_id_list,
        db_connection=None,
        dump_path=".",
        dump_database_name='so-dump.db'):
    is_create_connection = False
    cursor = None
    if db_connection is None:
        is_create_connection = True
        db_connection = build_connect_to_sqlite_with_row_factory(dump_path, dump_database_name)
    try:
        cursor = db_connection.cursor()
        sql = generate_select_question_id_list(min_id=min_id, max_id=max_id)
        cursor = cursor.execute(sql)
        return cursor_processor_func(cursor)
    except Exception, e:
        print e
    finally:
        if is_create_connection:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()


if __name__ == '__main__':
    fire.Fire(process_question_id_list)
