#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os

import fire

from db_util import build_connect_to_sqlite_with_row_factory, get_max_id
from sql_util import generate_select_question_id_list
from db_query import get_question_and_answers
from anatomy import CODE_BLOCK_QUERY_TYPE, TABLE_NAMES


def cursor_process_export_word2vec_corpus(cursor,
                                          output_file,
                                          db_connection,
                                          code_block_exist_type=CODE_BLOCK_QUERY_TYPE.HALF):
    for row in cursor.fetchall():
        question_id = row["Id"]
        question, answer_list = get_question_and_answers(question_id, code_block_exist_type, db_connection)
        output_file.write(question)
        output_file.write("\n")
        output_file.write("\n".join(answer_list))
        output_file.write("\n\n")


def process_question_id_list(
        output_file,
        db_connection,
        min_id=None,
        max_id=None,
        code_block_exist_type=CODE_BLOCK_QUERY_TYPE.HALF

):
    cursor = None
    try:
        cursor = db_connection.cursor()
        sql = generate_select_question_id_list(min_id=min_id, max_id=max_id)
        cursor = cursor.execute(sql)
        return cursor_process_export_word2vec_corpus(cursor=cursor,
                                                     output_file=output_file,
                                                     db_connection=db_connection,
                                                     code_block_exist_type=code_block_exist_type)
    except Exception, e:
        print e
    finally:
        if cursor:
            cursor.close()


def export_word2vec_corpus(
        output_file_name,
        output_file_path=".",
        max_id=None,
        step=50000,
        dump_path='.',
        dump_database_name='so-dump.db',
        code_block_exist_type=CODE_BLOCK_QUERY_TYPE.HALF,
):
    db_connection = None
    try:
        if max_id is None:
            max_id = get_max_id(dump_path, dump_database_name, TABLE_NAMES.POSTS, "Id")

        db_connection = build_connect_to_sqlite_with_row_factory(dump_path=dump_path,
                                                                 dump_database_name=dump_database_name)
        out_file_full_path = os.path.join(output_file_path, output_file_name)

        with codecs.open(out_file_full_path, 'a', encoding='utf-8') as output:
            for startId in range(0, max_id, step):
                endId = min(startId + step, max_id)
                process_question_id_list(output_file=output,
                                         db_connection=db_connection,
                                         min_id=startId,
                                         max_id=endId,
                                         code_block_exist_type=code_block_exist_type)
                print "done ", startId, "-", endId

    except Exception, error:
        print error
    finally:
        if db_connection:
            db_connection.close()


if __name__ == '__main__':
    fire.Fire(export_word2vec_corpus)
