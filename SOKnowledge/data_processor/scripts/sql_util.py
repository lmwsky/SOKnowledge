#!/usr/bin/python
# -*- coding: utf-8 -*-
import fire

from anatomy import search_table_anatomy, TABLE_NAMES, CODE_BLOCK_TYPE


def generate_select_question_id_list(min_id=None, max_id=None):
    sql = "SELECT Id FROM {table} WHERE ".format(table=TABLE_NAMES.POSTS)
    condition_list = []
    if max_id:
        condition_list.append("Id<={max_id}".format(max_id=max_id))
    if min_id:
        condition_list.append("Id>{min_id}".format(min_id=min_id))
    condition_list.append("PostTypeId=1")
    return sql + " AND ".join(condition_list)


def generate_create_sql_for_anatomy(anatomy):
    create_query = 'CREATE TABLE IF NOT EXISTS {table} ({fields})'
    fields = ", ".join(['{0} {1}'.format(name, field_type) for name, field_type in anatomy['normal_field'].items()])
    if anatomy['primary_key_name']:
        primary_str = '{0} {1} PRIMARY KEY'.format(anatomy['primary_key_name'], anatomy['primary_key_type'])
        if anatomy['autoincrement']:
            primary_str = "{0} AUTOINCREMENT".format(primary_str)
        fields = "{0}, {1}".format(primary_str, fields)
    sql_create = create_query.format(table=anatomy['table_name'], fields=fields)
    return sql_create


def generate_insert_sql_for_anatomy(anatomy):
    insert_query = 'INSERT INTO {table} ({columns}) VALUES ({values})'

    fields = ', '.join([field_name for field_name in anatomy['normal_field'].keys()])
    field__keys_ = ('?, ' * len(anatomy['normal_field'].keys()))[:-2]

    if anatomy['primary_key_name'] and not anatomy['autoincrement']:
        fields = "{0}, {1}".format(anatomy['primary_key_name'], fields)
        field__keys_ += ', ?'
    return insert_query.format(
        table=anatomy['table_name'],
        columns=fields,
        values=field__keys_)


def generate_insert_sql_for_table(table_name):
    return generate_insert_sql_for_anatomy(search_table_anatomy(table_name))


def generate_create_sql_for_table(table_name):
    return generate_create_sql_for_anatomy(search_table_anatomy(table_name))


def generate_create_sql_for_tokenize_text(table_name):
    anatomy = search_table_anatomy(TABLE_NAMES.TOKENIZE_TABLE_NORMAL_FORM)
    create_query = 'CREATE TABLE IF NOT EXISTS {table} ({fields})'
    fields = ", ".join(['{0} {1}'.format(name, field_type) for name, field_type in anatomy['normal_field'].items()])
    if anatomy['primary_key_name']:
        primary_str = '{0} {1} PRIMARY KEY'.format(anatomy['primary_key_name'], anatomy['primary_key_type'])
        if anatomy['autoincrement']:
            primary_str = "{0} AUTOINCREMENT".format(primary_str)
        fields = "{0}, {1}".format(primary_str, fields)
    sql_create = create_query.format(table=table_name, fields=fields)
    return sql_create


def generate_insert_sql_for_tokenize_text(table_name):
    insert_query = 'INSERT INTO {table} ({columns}) VALUES ({values})'
    return insert_query.format(
        table=table_name,
        columns='Id, tokenize_text',
        values='?, ?')


if __name__ == '__main__':
    fire.Fire()


def get_query_code_block_sql(code_block_table, parent_id, code_block_type):
    if code_block_type == CODE_BLOCK_TYPE.SMALL or code_block_type == CODE_BLOCK_TYPE.LARGE:
        select_query = "SELECT * FROM {table} where ParentId={ParentId} and type={type}"
        return select_query.format(table=code_block_table, ParentId=parent_id, type=code_block_type)
    else:
        select_query = "SELECT * FROM {table} where ParentId={ParentId}"
        return select_query.format(table=code_block_table, ParentId=parent_id)
