#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
the structure of the stackOverflow table,
"""
import const

ANATOMY = {
    'posts_code_block': {
        'table_name': 'posts_code_block',
        'normal_field': {
            'codeBlockName': 'TEXT',
            'codeBlock': 'TEXT',
            'type': 'INTEGER',
             'ParentId': 'INTEGER'
},
        'primary_key_name': 'id',
        'primary_key_type': 'INTEGER',
        'autoincrement': True
    },
    'posts': {
        'table_name': 'posts',
        'normal_field': {
            'PostTypeId': 'INTEGER',  # 1: Question, 2: Answer
            'ParentID': 'INTEGER',  # (only present if PostTypeId is 2)
            'AcceptedAnswerId': 'INTEGER',  # (only present if PostTypeId is 1)
            'CreationDate': 'DATETIME',
            'Score': 'INTEGER',
            'ViewCount': 'INTEGER',
            'Body': 'TEXT',
            'OwnerUserId': 'INTEGER',  # (present only if user has not been deleted)
            'OwnerDisplayName': 'TEXT',
            'LastEditorUserId': 'INTEGER',
            'LastEditorDisplayName': 'TEXT',  # ="Rich B"
            'LastEditDate': 'DATETIME',  # ="2009-03-05T22:28:34.823"
            'LastActivityDate': 'DATETIME',  # ="2009-03-11T12:51:01.480"
            'CommunityOwnedDate': 'DATETIME',  # (present only if post is community wikied)
            'Title': 'TEXT',
            'Tags': 'TEXT',
            'AnswerCount': 'INTEGER',
            'CommentCount': 'INTEGER',
            'FavoriteCount': 'INTEGER',
            'ClosedDate': 'DATETIME'
        },
        'primary_key_name': 'Id',
        'primary_key_type': 'INTEGER',
        'autoincrement': False,
    },
    'remove_tag_posts_body': {
        'table_name': 'remove_tag_posts_body',
        'normal_field': {
            'RemoveTagBody': 'TEXT'
        },
        'primary_key_name': 'Id',
        'primary_key_type': 'INTEGER',
        'autoincrement': False,
    },
    'tokenize_remove_tag_posts_body': {
        'table_name': 'tokenize_remove_tag_posts_body',
        'normal_field': {
            'TokenizeRemoveTagBody': 'TEXT'
        },
        'primary_key_name': 'Id',
        'primary_key_type': 'INTEGER',
        'autoincrement': False,
    },
    'tokenize_text_table': {
        'table_name': 'tokenize_text_table',
        'normal_field': {
            'tokenize_text': 'TEXT'
        },
        'primary_key_name': 'Id',
        'primary_key_type': 'INTEGER',
        'autoincrement': False,
    },
}

TABLE_NAMES = const.Const()
TABLE_NAMES.POSTS = 'posts'
TABLE_NAMES.POSTS_CODE_BLOCK = 'posts_code_block'
TABLE_NAMES.REMOVE_TAG_POSTS_BODY = 'remove_tag_posts_body'
TABLE_NAMES.TOKENIZE_REMOVE_TAG_POSTS_BODY = 'tokenize_remove_tag_posts_body'
TABLE_NAMES.TOKENIZE_TABLE_NORMAL_FORM = 'tokenize_text_table'


def search_table_anatomy(table_name):
    """
    get the anatomy of specific table name
    :param table_name: the name of the table
    :return: the anatomy of the table name,None if not exist
    """
    return ANATOMY[table_name]
