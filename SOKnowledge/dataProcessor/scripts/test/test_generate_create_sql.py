from unittest import TestCase

from SOKnowledge.data_processor.scripts.finish.sql_util import generate_create_sql, generate_insert_sql


class TestGenerate_create_sql(TestCase):
    ANATHOMY = {
        'table_name': 'postsBlock',
        'normal_field': {
            'ParentId': 'INTEGER',
            'codeBlockName': 'TEXT',
            'codeBlock': 'TEXT',
            'type': 'INTEGER'
        },
        'primary_key_name': 'id',
        'primary_key_type': 'INTEGER',
        'autoincrement': True
    }
    def test_generate_create_sql(self):

        sql = generate_create_sql(TestGenerate_create_sql.ANATHOMY)
        correct_sql = 'CREATE TABLE IF NOT EXISTS postsBlock (id INTEGER PRIMARY KEY AUTOINCREMENT, codeBlock TEXT, type INTEGER, codeBlockName TEXT, ParentId INTEGER)'
        self.assertEqual(sql, correct_sql)

    def test_generate_insert_sql(self):
        sql=generate_insert_sql(TestGenerate_create_sql.ANATHOMY)
        correct_sql = 'INSERT INTO postsBlock (codeBlock, type, codeBlockName, ParentId) VALUES (?, ?, ?, ?)'
        self.assertEqual(sql, correct_sql)
