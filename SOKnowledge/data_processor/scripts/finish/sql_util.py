#!/usr/bin/python
# -*- coding: utf-8 -*-
import fire

from anatomy import search_table_anatomy, TABLE_NAMES


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

    return insert_query.format(
        table=anatomy['table_name'],
        columns=', '.join([field_name for field_name in anatomy['normal_field'].keys()]),
        values=('?, ' * len(anatomy['normal_field'].keys()))[:-2])


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
