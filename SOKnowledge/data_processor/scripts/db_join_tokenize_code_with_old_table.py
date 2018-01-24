import logging
import os
import sqlite3

import fire

from anatomy import TABLE_NAMES


def join_tokenize_code_text_to_old_table(dump_path='.',
                                         dump_database_name='so-dump.db',
                                         log_filename='so-parser.log', ):
    """
    create a new table CODE_BLOCK_WITH_TOKENIZE_CODE,the data in it are
    the join  result of the tokenize code block text and posts_code_block table,
    and delete the posts_code_block
    :param dump_path:
    :param dump_database_name:
    :param log_filename:
    :return:
    """
    db = None
    try:
        logging.basicConfig(filename=os.path.join(dump_path, log_filename), level=logging.INFO)

        db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
        table_name = TABLE_NAMES.CODE_BLOCK_WITH_TOKENIZE_CODE
        sql_query = "CREATE TABLE IF NOT EXISTS {table} AS SELECT posts_code_block.id as Id,ParentId,type,codeBlockName,codeBlock,tokenize_text from posts_code_block INNER JOIN tokenize_codeBlock_for_posts_code_block ON posts_code_block.id=tokenize_codeBlock_for_posts_code_block.Id"
        sql = sql_query.format(table=table_name)
        db.execute(sql)
        db.execute("DROP TABLE posts_code_block")
        db.commit()
    except Exception, error:
        print error
        logging.warning(error)
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    fire.Fire(join_tokenize_code_text_to_old_table)
