#!/usr/bin/python
# -*- coding: utf-8 -*-
import fire

from anatomy import TABLE_NAMES
from db_util import process_table_data
from sql_util import generate_insert_sql_for_table, \
    generate_create_sql_for_table
from SOKnowledge.data_processor.scripts.finish.text_processor import remove_tags


def cursor_process_remove_tag_for_posts(cursor, process_func_extra_params=None):
    sql_values_dict = {}
    post_row_values = []
    all_code_blocks = []
    for row in cursor:
        [new_posts_row_value, code_blocks] = row_process_remove_tag_for_posts(row)
        post_row_values.append(new_posts_row_value)
        all_code_blocks = all_code_blocks + code_blocks

    create_sql_list = [generate_create_sql_for_table(TABLE_NAMES.REMOVE_TAG_POSTS_BODY),
                       generate_create_sql_for_table(TABLE_NAMES.POSTS_CODE_BLOCK)]

    sql_values_dict[generate_insert_sql_for_table(TABLE_NAMES.REMOVE_TAG_POSTS_BODY)(
        TABLE_NAMES.REMOVE_TAG_POSTS_BODY)] = post_row_values
    sql_values_dict[generate_insert_sql_for_table(TABLE_NAMES.POSTS_CODE_BLOCK)] = all_code_blocks

    return sql_values_dict, create_sql_list


def row_process_remove_tag_for_posts(row):
    body = row['Body']
    id = row['Id']
    result_dict = remove_tags(body)

    new_posts_row_value = [id, result_dict['cleanText']]

    large_code_block = [[code_block_name, code_block, 1] for code_block_name, code_block in
                        result_dict['largeCodeDict'].items()]
    small_code_block = [[code_block_name, code_block, 0] for code_block_name, code_block in
                        result_dict['smallCodeDict'].items()]

    code_blocks = large_code_block + small_code_block

    return new_posts_row_value, code_blocks


def db_remove_tags_for_posts(
        dump_path='.',
        dump_database_name='so-dump.db',
        log_filename='so-parser.log',
):
    process_table_data(TABLE_NAMES.POSTS,
                       cursor_process_remove_tag_for_posts,
                       dump_path,
                       dump_database_name,
                       log_filename)


if __name__ == '__main__':
    fire.Fire(db_remove_tags_for_posts)
