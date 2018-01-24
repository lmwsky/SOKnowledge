"""annotator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
app_name = 'tagger'

urlpatterns = [
    url(r'^ner_tagger/$', views.ner_tagger, name='ner_tagger'),
    url(r'^ner_tagger/(?P<text>[\s\S]+)/result/$', views.ner_tagger_result, name='ner_tagger_result'),
    url(r'^cbr_tagger/$', views.code_block_tagger, name='code_block_tagger'),
    url(r'^cbr_tagger/(?P<text>[\s\S]+)/result/$', views.code_block_tagger_result, name='code_block_tagger_result'),
    url(r'^cbt_tagger/$', views.code_block_type_tagger, name='code_block_type_tagger'),
    url(r'^cbt_tagger/(?P<text>[\s\S]+)/result/$', views.code_block_type_tagger_result, name='code_block_type_tagger_result'),


]
