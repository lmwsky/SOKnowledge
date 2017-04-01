#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse

from annotator.annotator_util import get_need_tagged_text, save_as_ner_annotation
from SOKnowledge.ner_util.format_util import __labels__
from annotator.form.tagged_text_form import TaggedTextForm
from annotator.query_util import get_post_tokenize_remove_tag_body_with_small_code_block, get_annotation
from models import TokenizeRemovetagbodyForRemoveTagPostsBody, Posts

PER_PAGE = 25


def index(request):
    latest_posts_list = Posts.objects.all()[:10]
    template = loader.get_template('annotator/index.html')
    context = {
        'latest_posts_list': latest_posts_list,
    }
    return HttpResponse(template.render(context, request))


def post_detail(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    tokenize_post = get_object_or_404(TokenizeRemovetagbodyForRemoveTagPostsBody, pk=post_id)
    return render(request, 'annotator/detail.html', {'post': post, 'tokenize_post': tokenize_post})


def ner_annotator(request, post_id):
    text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)

    default_data = {'post_id': post_id, 'input_text': text}
    form = TaggedTextForm(default_data)

    return render(request, 'annotator/ner_annotator.html', {
        'form': form,
        'postId': post_id,
        'labels': __labels__,
        'labels_data_for_js': json.dumps(__labels__),
        'text': text})


def process_ner_annotator_question(request, question_index):
    print 'first request.POST=', request.POST
    print 'first question_index=', question_index

    question_index = int(question_index)
    answer_index = -1
    if request.method == 'POST':
        form = TaggedTextForm(request.POST)
        print 'post=',request.POST
        if form.is_valid():
            text = form.cleaned_data['input_text']
            post_id = form.cleaned_data['post_id']
            save_as_ner_annotation(post_id, text)
            return redirect(reverse('annotator:ner_annotator_question', args=[question_index, ]))

    return HttpResponse("submit not ok")


def ner_annotator_question(request, question_index):

    question_index = int(question_index)
    answer_index = -1
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
    return render(request, 'annotator/ner_annotator.html', {
        'post_type':1,
        'question_index': question_index,
        'answer_index': answer_index,
        'form': form,
        'postId': question_post.id,
        'labels': __labels__,
        'labels_data_for_js': json.dumps(__labels__),
        'text': text,
        'current_question_index': question_index,
        'current_answer_index': -1
    })


def process_ner_annotator_answer(request, question_index, answer_index):
    question_index = int(question_index)
    answer_index = int(answer_index)
    if request.method == 'POST':
        form = TaggedTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            post_id = form.cleaned_data['post_id']
            save_as_ner_annotation(post_id, text)
            return redirect(reverse('annotator:ner_annotator_answer', args=[question_index, answer_index]))
    return HttpResponse("submit not ok")


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

    return render(request, 'annotator/ner_annotator.html', {
        'post_type': 2,
        'question_index': question_index,
        'answer_index': answer_index,
        'form': form,
        'postId': post_id,
        'labels': __labels__,
        'labels_data_for_js': json.dumps(__labels__),
        'text': text,
        'current_question_index': question_index,
        'current_answer_index': answer_index
    })


def listing_question(request, page):
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
                                                            })


def listing_answer_for_question(request, question_index, page):
    question_index = int(question_index)
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
    })
