from unittest import TestCase

from SOKnowledge.data_processor.scripts.finish.sql_util import generate_insert_sql_for_tokenize_text, \
    generate_create_sql_for_tokenize_text


class Test_sql_util(TestCase):
    def test_generate_insert_sql_for_tokenize_text(self):
        self.assertEqual(generate_insert_sql_for_tokenize_text('tokenize_post'),
                         "INSERT INTO tokenize_post (Id, tokenize_text) VALUES (?, ?)")

    def test_generate_create_sql_for_tokenize_text(self):
        self.assertEqual(generate_create_sql_for_tokenize_text('tokenize_post'),
                         "CREATE TABLE IF NOT EXISTS tokenize_post (Id INTEGER PRIMARY KEY, tokenize_text TEXT)")
