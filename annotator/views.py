#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django import forms

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse

from annotator.annotator_util import get_need_tagged_text, save_as_ner_annotation, get_sentence_tye_annotations, \
    __sentence_type_list__
from SOKnowledge.ner_util.format_util import __labels__
from annotator.form.sentence_type_annotation_form import SentenceTypeAnnotationForm
from annotator.form.tagged_text_form import TaggedTextForm
from annotator.query_util import get_post_tokenize_remove_tag_body_with_small_code_block, get_annotation, \
    get_all_large_code_block
from models import TokenizeRemovetagbodyForRemoveTagPostsBody, Posts, SentenceTypeAnnotation

BEFORE_ANSWER = -1

POST_TYPE_QUESTION = 1

POST_TYPE_ANSWER = 2

PER_PAGE = 25


def ner_annotator_question(request, question_index):
    question_index = int(question_index)
    answer_index = BEFORE_ANSWER
    if request.method == 'POST':
        form = TaggedTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            post_id = form.cleaned_data['post_id']
            save_as_ner_annotation(post_id, text)
            return redirect(reverse('annotator:ner_annotator_question', kwargs={'question_index': question_index}))

    question_post = Posts.objects.filter(posttypeid=1)[question_index]
    post_id = question_post.id

    text = get_need_tagged_text(post_id)

    default_data = {'post_id': question_post.id, 'input_text': text}
    form = TaggedTextForm(default_data)
    code_block_list=get_all_large_code_block(post_id)

    return render(request, 'annotator/ner_annotator.html', {
        'post_type': POST_TYPE_QUESTION,
        'question_index': question_index,
        'answer_index': answer_index,
        'form': form,
        'postId': question_post.id,
        'labels': __labels__,
        'labels_data_for_js': json.dumps(__labels__),
        'text': text,
        'code_block_list':code_block_list,
    })


def ner_annotator_answer(request, question_index, answer_index):
    question_index = int(question_index)
    answer_index = int(answer_index)
    if request.method == 'POST':
        form = TaggedTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            post_id = form.cleaned_data['post_id']
            save_as_ner_annotation(post_id, text)
            return redirect(reverse('annotator:ner_annotator_answer', args=[question_index, answer_index]))
    question_post = Posts.objects.filter(posttypeid=1)[question_index]
    answer_post = Posts.objects.filter(parentid=question_post.id)[answer_index]
    post_id = answer_post.id

    text = get_need_tagged_text(post_id)

    default_data = {'post_id': post_id, 'input_text': text}
    form = TaggedTextForm(default_data)

    code_block_list=get_all_large_code_block(post_id)

    return render(request, 'annotator/ner_annotator.html', {
        'post_type': POST_TYPE_ANSWER,
        'question_index': question_index,
        'answer_index': answer_index,
        'form': form,
        'postId': post_id,
        'labels': __labels__,
        'labels_data_for_js': json.dumps(__labels__),
        'text': text,
        'code_block_list':code_block_list,
    })


def listing_question_for_annotator(request, page, annotator_type):
    annotator_type = int(annotator_type)
    question_post_list = Posts.objects.filter(posttypeid=1)
    paginator = Paginator(question_post_list, PER_PAGE)  # Show 25 contacts per page
    try:
        question_post_sub_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_post_sub_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_post_sub_list = paginator.page(paginator.num_pages)
    return render(request, 'annotator/question_list.html', {'question_post_list': question_post_sub_list,
                                                            'annotator_type': annotator_type
                                                            })


def listing_answer_for_question_for_annotator(request, question_index, page, annotator_type):
    question_index = int(question_index)
    annotator_type = int(annotator_type)
    question_post = Posts.objects.filter(posttypeid=1)[question_index]

    answer_post_list = Posts.objects.filter(parentid=question_post.id)

    paginator = Paginator(answer_post_list, PER_PAGE)  # Show 25 contacts per page
    try:
        answer_post_sub_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answer_post_sub_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answer_post_sub_list = paginator.page(paginator.num_pages)
    return render(request, 'annotator/answer_list_for_question.html', {
        'question_index': question_index,
        'answer_post_list': answer_post_sub_list,
        'annotator_type': annotator_type
    })


def sentences_annotator_question(request, question_index):
    question_index = int(question_index)
    answer_index = BEFORE_ANSWER
    question_post = Posts.objects.filter(posttypeid=1)[question_index]
    post_id = question_post.id

    SentenceTypeAnnotationFormSet = inlineformset_factory(Posts, SentenceTypeAnnotation,
                                                          extra=0,
                                                          can_delete=False,
                                                          form=SentenceTypeAnnotationForm,
                                                          fields=('annotation_text', 'sentence_type'),

                                                          )

    if request.method == 'POST':
        formset = SentenceTypeAnnotationFormSet(request.POST, request.FILES, instance=question_post)
        if formset.is_valid():
            for form in formset:
                annotation = form.save(commit=False)
                annotation.valid = True
                annotation.save()

            return redirect(
                reverse('annotator:sentences_annotator_question', kwargs={'question_index': question_index}))

    text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
    code_block_list=get_all_large_code_block(post_id)

    sentence_type_annotations = get_sentence_tye_annotations(post_id)
    if sentence_type_annotations:
        formset = SentenceTypeAnnotationFormSet(instance=Posts.objects.get(id=post_id))
    else:
        raise Http404('post is not exist')
    return render(request, 'annotator/sentences_annotator.html', {
        'post_type': POST_TYPE_QUESTION,
        'sentence_type_list': __sentence_type_list__,
        'question_index': question_index,
        'answer_index': answer_index,
        'formset': formset,
        'postId': question_post.id,
        'text': text,
        'code_block_list':code_block_list,
    })


def sentences_annotator_answer(request, question_index, answer_index):
    question_index = int(question_index)
    answer_index = int(answer_index)
    question_post = Posts.objects.filter(posttypeid=1)[question_index]
    answer_post = Posts.objects.filter(parentid=question_post.id)[answer_index]
    post_id = answer_post.id

    SentenceTypeAnnotationFormSet = inlineformset_factory(Posts, SentenceTypeAnnotation,
                                                          extra=0,
                                                          can_delete=False,
                                                          form=SentenceTypeAnnotationForm,
                                                          fields=('annotation_text', 'sentence_type'),

                                                          )

    if request.method == 'POST':
        formset = SentenceTypeAnnotationFormSet(request.POST, request.FILES, instance=question_post)
        if formset.is_valid():
            for form in formset:
                annotation = form.save(commit=False)
                annotation.valid = True
                annotation.save()

            return redirect(
                reverse('annotator:sentences_annotator_question',
                        kwargs={'question_index': question_index, 'answer_index': answer_index}))

    text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
    code_block_list=get_all_large_code_block(post_id)
    sentence_type_annotations = get_sentence_tye_annotations(post_id)
    if sentence_type_annotations:
        formset = SentenceTypeAnnotationFormSet(instance=Posts.objects.get(id=post_id))
    else:
        raise Http404('post is not exist')
    return render(request, 'annotator/sentences_annotator.html', {
        'post_type': POST_TYPE_ANSWER,
        'sentence_type_list': __sentence_type_list__,
        'question_index': question_index,
        'answer_index': answer_index,
        'formset': formset,
        'postId': post_id,
        'text': text,
        'code_block_list':code_block_list,
    })
