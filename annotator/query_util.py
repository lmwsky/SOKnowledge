# !/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from SOKnowledge.data_processor.scripts.nlp_util import word_tokenize_nltk
from annotator.models import Posts, CodeBlockWithTokenizeCode, TokenizeRemovetagbodyForRemoveTagPostsBody


def get_all_answer(question_id):
    try:
        return Posts.objects.all().filter(parentid=question_id)
    except Exception, error:
        return []


def get_question_list(offset=None, num=None):
    if offset and num:
        return Posts.objects.all().filter(posttypeid=1)[offset:offset + num]
    else:
        if num:
            return Posts.objects.all().filter(posttypeid=1)[:num]
        else:
            return Posts.objects.all().filter(posttypeid=1)


def get_all_code_block(post_id, code_block_type=-1):
    try:
        if code_block_type == -1:
            return CodeBlockWithTokenizeCode.objects.filter(parent_id=post_id)
        else:
            return CodeBlockWithTokenizeCode.objects.filter(parent_id=post_id).filter(type=code_block_type)
    except Exception, error:
        return []


def get_post(post_id):
    return Posts.objects.get(id=post_id)


def get_post_tokenize_remove_tag_body(post_id):
    try:
        tokenize_post_body = TokenizeRemovetagbodyForRemoveTagPostsBody.objects.get(id=post_id)
        if tokenize_post_body:
            return tokenize_post_body.tokenize_text
        else:
            return ""
    except Exception, error:
        return ""


def get_post_tokenize_remove_tag_body_with_small_code_block(post_id):
    try:
        tokenize_post_body = TokenizeRemovetagbodyForRemoveTagPostsBody.objects.get(id=post_id)
        if tokenize_post_body:
            text = tokenize_post_body.tokenize_text
            code_block_list = get_all_code_block(post_id, code_block_type=CodeBlockWithTokenizeCode.SMALL_CODE_BLOCK)
            for code_block in code_block_list:
                text = text.replace(code_block.code_block_name, code_block.tokenize_text)
            return text
        else:
            return ""

    except Exception, error:
        return ""


def get_post_tokenize_remove_tag_body_with_all_code_block(post_id):
    try:
        tokenize_post_body = TokenizeRemovetagbodyForRemoveTagPostsBody.objects.get(id=post_id)
        if tokenize_post_body:
            text = tokenize_post_body.tokenize_text
            code_block_list = get_all_code_block(post_id)
            for code_block in code_block_list:
                text = text.replace(code_block.code_block_name, code_block.tokenize_text)
            return text
        else:
            return ""
    except Exception, error:
        return ""


def get_question(question_id):
    return Posts.objects.get(id=question_id)


POST_TEXT_TYPE_HTML = 0
POST_TEXT_TYPE_TOKENIZE_NO_CODE_BLOCK = 1
POST_TEXT_TYPE_TOKENIZE_WITH_SMALL_CODE_BLOCK = 2
POST_TEXT_TYPE_TOKENIZE_WITH_ALL_CODE_BLOCK = 3


def get_post_text(post, post_text_type=POST_TEXT_TYPE_TOKENIZE_WITH_SMALL_CODE_BLOCK):
    if post:
        if post_text_type == POST_TEXT_TYPE_HTML:
            return post.body
        if post_text_type == POST_TEXT_TYPE_TOKENIZE_NO_CODE_BLOCK:
            return get_post_tokenize_remove_tag_body(post.id)
        if post_text_type == POST_TEXT_TYPE_TOKENIZE_WITH_SMALL_CODE_BLOCK:
            return get_post_tokenize_remove_tag_body_with_small_code_block(post.id)
        if post_text_type == POST_TEXT_TYPE_TOKENIZE_WITH_ALL_CODE_BLOCK:
            return get_post_tokenize_remove_tag_body_with_all_code_block(post.id)
    return None


def export_word2vec_corpus_by_title_question_answers_order(num=100,
                                                           offset=0,
                                                           post_text_type=POST_TEXT_TYPE_TOKENIZE_WITH_SMALL_CODE_BLOCK,
                                                           output_file_path=".",
                                                           output_file_name="corpus.txt"):
    """
    usage:use in shell,
    0:python manage.py shell
    In [1]: import django

    In [2]: django.setup()

    In [3]: from annotator.query_util import export_questions

    In [5]: export_questions(num=None)
    """
    question_num = 0
    answer_num = 0
    out_file_full_path = os.path.join(output_file_path, output_file_name)
    with codecs.open(out_file_full_path, 'w', encoding='utf-8') as output:
        question_list = get_question_list(offset=offset, num=num)
        for question in question_list:
            if question.title:
                output.write(" ".join(word_tokenize_nltk(question.title)) + "\n")
            post_text = get_post_text(question, post_text_type)
            if post_text:
                if question_num % 10000 == 0:
                    print 'finish ', 'question=', question_num, ' answer=', answer_num
                question_num += 1
                output.write(post_text)
                answer_list = get_all_answer(question.id)
                for answer in answer_list:
                    answer_num += 1
                    post_text = get_post_text(answer, post_text_type)
                    output.write(post_text)
                output.write("\n")

    print 'export ', 'question=', question_num, ' answer=', answer_num
