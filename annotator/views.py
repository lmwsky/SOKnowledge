#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from models import TokenizeRemovetagbodyForRemoveTagPostsBody, Posts


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
