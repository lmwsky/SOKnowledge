#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import sqlite3


def execute_batch(data_base_full_path, sql, values):
    db = None
    cursor = None
    try:
        db = sqlite3.connect(data_base_full_path)
        cursor = db.cursor()
        cursor.executemany(sql, values)
        db.commit()
    except Exception, error:
        print error
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def get_max_id(dump_path,
               dump_database_name,
               table_name,
               primary_key_name='id'):
    """
    get the max primary key of one table in sqlite database
    :param dump_path: the direction of the .db file
    :param dump_database_name: the name of the .db file,ect.="so.db"
    :param table_name: the name of the query table
    :param primary_key_name: the name of the primary key,default is 'id'
    :return: the max value of the primary key, if exception occurs,return None
    """
    select_query = "SELECT max({id}) as id from {table}"
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    sql = select_query.format(id=primary_key_name, table=table_name)
    try:
        cursor = db.execute(sql)
        for row in cursor:
            return row[0]
    except Exception, e:
        print e
    finally:
        if db:
            db.close()


def process_table_data(
        table_name,
        process_func,
        dump_path='.',
        dump_database_name='so-dump.db',
        log_filename='so-process.log',
        select_query='SELECT * FROM {table}',
        process_func_extra_params=None
):
    try:
        logging.basicConfig(filename=os.path.join(dump_path, log_filename), level=logging.INFO)
        dump_full_path = os.path.join(dump_path, dump_database_name)
        db = sqlite3.connect(dump_full_path)
        db.row_factory = sqlite3.Row
        query = select_query.format(table=table_name)
        cursor = db.execute(query)
        if cursor:
            sql_batch_input_dict, create_sql_list = process_func(cursor, process_func_extra_params)
            cursor.close()
            for sql in create_sql_list:
                db.execute(sql)
            for sql, values in sql_batch_input_dict.items():
                execute_batch(dump_full_path, sql, values)
        if db:
            db.commit()
            db.close()

    except Exception, error:
        logging.warning(error)
        print error


def build_connect_to_sqlite_with_row_factory(dump_database_name, dump_path):
    dump_full_path = os.path.join(dump_path, dump_database_name)
    db_connection = sqlite3.connect(dump_full_path)
    db_connection.row_factory = sqlite3.Row
    return db_connection
