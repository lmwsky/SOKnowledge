#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the annotator index.")
