#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from annotator.query_util import get_post_tokenize_remove_tag_body_with_small_code_block
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


__labels__ = [
    {'textLabel': 'API',
     'description': 'one api in program,ex. Integer.parseInt()',
     'value': 'api',
     },
    {'textLabel': 'PLAT',
     'description': 'one platform,ex.Linux,android,Windows 10',
     'value': 'platform',
     },
    {'textLabel': 'Fram',
     'description': 'Frame used in program, ect.django,ionic, ',
     'value': 'frame',
     },
    {'textLabel': 'PL',
     'description': 'program language,ex.JAVA,C++',
     'value': 'language',
     },
    {'textLabel': 'Stan',
     'description': 'like http,xml',
     'value': 'standard',
     },

]


def ner_annotator(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    tokenize_post = get_object_or_404(TokenizeRemovetagbodyForRemoveTagPostsBody, pk=post_id)
    text = get_post_tokenize_remove_tag_body_with_small_code_block(post_id)
    return render(request, 'annotator/ner_annotator.html', {'postId': post_id,
                                                            'labels': __labels__,
                                                            'labels_data_for_js': json.dumps(__labels__),
                                                            'text': text})
