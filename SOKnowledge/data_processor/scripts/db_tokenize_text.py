#!/usr/bin/python
# -*- coding: utf-8 -*-
import fire

from db_util import process_table_data, get_max_id
from nlp_util import sent_word_tokenize_nltk
from sql_util import generate_create_sql_for_tokenize_text, \
    generate_insert_sql_for_tokenize_text


def generate_tokenize_table_name(source_table_name, col_name="text"):
    """
    generate a new table name for tokenize text
    :param source_table_name: the source table name
    :param col_name: the tokenize text column
    :return: the new table name
    """
    return "tokenize_" + col_name + "_for_" + source_table_name


def cursor_process_tokenize_text(cursor, process_func_extra_params=None):
    if process_func_extra_params:
        return cursor_process_tokenize_text_specific_param(cursor,
                                                           process_func_extra_params['source_table_name'],
                                                           process_func_extra_params['tokenize_col_name'],
                                                           process_func_extra_params['primary_key_name'])
    else:
        raise Exception("process_func_extra_params is not specified")


def cursor_process_tokenize_text_specific_param(cursor, source_table_name, tokenize_col_name, primary_key_name="Id"):
    tokenize_table_name = generate_tokenize_table_name(source_table_name, tokenize_col_name)
    sql_values_dict = {}
    row_values = []

    for row in cursor.fetchall():
        try:
            new_tokenize_row_value = row_process_tokenize_text(row, tokenize_col_name, primary_key_name)
            row_values.append(new_tokenize_row_value)
        except Exception, e:
            print e, ' happen when ', primary_key_name, '=', row[primary_key_name]
    create_sql_list = [generate_create_sql_for_tokenize_text(tokenize_table_name)]
    sql_values_dict[generate_insert_sql_for_tokenize_text(tokenize_table_name)] = row_values

    return sql_values_dict, create_sql_list


def row_process_tokenize_text(row, tokenize_col_name, primary_key_name="Id",
                              word_tokenize_func=sent_word_tokenize_nltk):
    body = row[tokenize_col_name]
    id = row[primary_key_name]
    new_row_value = [id, word_tokenize_func(body)]
    return new_row_value


def db_process_tokenize_text(
        table_name,
        col_name,
        step=500000,
        max_id=None,
        primary_key_name="Id",
        dump_path='.',
        dump_database_name='so-dump.db',
        log_filename='so-parser.log',
):
    """
    tokenize a column of text value from database table,and create new table to store it
    :param table_name: the tokenized table name
    :param col_name: the tokenized column name
    :param primary_key_name: the primary key of the table,default is 'Id'
    :param dump_path:  the dir path of db file,default '.'
    :param dump_database_name: the name of db file,default 'so-dump.db'
    :param log_filename: the name of log file,default 'so-parser.log'
    :return:
    """
    if max_id is None:
        max_id = get_max_id(dump_path, dump_database_name, table_name, primary_key_name)
    select_query = "SELECT * FROM {table}"
    condition_clause = " where {primary_key}>{startId} AND {primary_key}<={endId}"
    for startId in range(0, max_id, step):
        endId = min(startId + step, max_id)
        sql = select_query + condition_clause.format(startId=startId, endId=endId, primary_key=primary_key_name)

        cursor_process_tokenize_text_extra_params = {'source_table_name': table_name,
                                                     'tokenize_col_name': col_name,
                                                     'primary_key_name': primary_key_name}
        process_table_data(table_name,
                           cursor_process_tokenize_text,
                           dump_path,
                           dump_database_name,
                           log_filename,
                           process_func_extra_params=cursor_process_tokenize_text_extra_params,
                           select_query=sql)
        print 'done ', startId, '-', endId


if __name__ == '__main__':
    fire.Fire(db_process_tokenize_text)
