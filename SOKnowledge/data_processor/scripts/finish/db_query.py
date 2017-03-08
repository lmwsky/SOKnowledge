#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3

import fire

from anatomy import TABLE_NAMES


def get_question_id(process_id_func,
                    db=None,
                    dump_path=".",
                    dump_database_name='so-dump.db',
                    select_query="SELECT * FROM {table} WHERE PostTypeId=1 LIMIT 1000",
                    table_name=TABLE_NAMES.POSTS):
    if db is None:
        dump_full_path = os.path.join(dump_path, dump_database_name)
        db = sqlite3.connect(dump_full_path)
    try:
        cusor = db.cursor()

    except Exception, e:
        print e


def get_all_answers_for_question(
        question_id,
        dump_path=".",
        db=None,
        dump_database_name='so-dump.db',
        select_query="SELECT * FROM {table} WHERE ParentID={question_id}",
        table_name=TABLE_NAMES.POSTS):
    if db is None:
        dump_full_path = os.path.join(dump_path, dump_database_name)
        print dump_full_path
        db = sqlite3.connect(dump_full_path)
    try:
        cursor = db.cursor()
        sql = select_query.format(table=table_name, question_id=question_id)
        result_cursor = cursor.execute(sql)
        return result_cursor
    except Exception, e:
        print e


if __name__ == '__main__':
    fire.Fire(get_all_answers_for_question)
