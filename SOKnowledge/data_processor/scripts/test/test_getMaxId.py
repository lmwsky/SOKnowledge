#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase

from SOKnowledge.data_processor.scripts.db_util import get_max_id


class TestGetMaxId(TestCase):
    def test_getMaxId(self):
        dump_path = u'E:\实验室\data'
        dump_database_name = u'so-dump.db'
        table_name = 'posts'
        primary_key_name = 'Id'
        max_id = get_max_id(dump_path, dump_database_name, table_name, primary_key_name)
        self.assertEqual(max_id, 34573264)

        max_id = get_max_id(dump_path, dump_database_name, table_name, 'unExistColumn')
        self.assertIsNone(max_id)
