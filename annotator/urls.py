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

app_name = 'annotator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^ner/(?P<post_id>[0-9]+)/$', views.ner_annotator, name='ner_annotator'),
    url(r'^ner/(?P<question_index>[0-9]+)/question$', views.ner_annotator_question, name='ner_annotator_question'),

    url(r'^ner/(?P<question_index>[0-9]+)/(?P<answer_index>[0-9]+)/answer$', views.ner_annotator_answer,
        name='ner_annotator_answer'),
    url(r'^ner/question/page/(?P<page>[0-9]+)/$', views.listing_question, name='listing_question'),
    url(r'^ner/question/(?P<question_index>[0-9]+)/answer/page/(?P<page>[0-9]+)/$', views.listing_answer_for_question,
        name='listing_answer_for_question'),

    url(r'^ner/(?P<question_index>[0-9]+)/question/submit$', views.process_ner_annotator_question,
        name='process_ner_annotator_question'),
    url(r'^ner/(?P<question_index>[0-9]+)/(?P<answer_index>[0-9]+)/answer/submit$', views.process_ner_annotator_answer,
        name='process_ner_annotator_answer'),
]
