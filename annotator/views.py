#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# Create your views here.
from django.http import HttpResponse
from models import TokenizeRemovetagbodyForRemoveTagPostsBody


def index(request):
    latest_posts_list = TokenizeRemovetagbodyForRemoveTagPostsBody.objects.all()[:10]
    output = '\n\n---------------\n\n'.join([post.tokenize_text for post in latest_posts_list])
    return HttpResponse(output)
