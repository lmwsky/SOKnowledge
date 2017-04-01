import json
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from SOKnowledge.ner_util.tagger import NERTagger
from SOKnowledge.settings import BASE_DIR
from form.multi_line_text_form import MultiLineTextForm
from SOKnowledge.ner_util.format_util import __labels__, build_conll_format_for_sentences, \
    build_html_format_for_sentences, \
    build_se_format_for_sentences

__ner_tagger__ = NERTagger()
__ner_tagger__.load_model(os.path.join(BASE_DIR, 'SOKnowledge/ner_util', 'models/so_for_epochs50_splitwords'))


def ner_tagger(request):
    if request.method == 'POST':
        form = MultiLineTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            return HttpResponseRedirect(reverse('tagger:ner_tagger_result', args=(text,)))
    else:
        form = MultiLineTextForm()
        return render(request, 'tagger/ner_tagger_form.html', {'form': form})


def ner_tagger_result(request, text):
    words_list, tags_list = __ner_tagger__.tag(text)

    conll_format_text = build_conll_format_for_sentences(words_list, tags_list)
    html_format_text = build_html_format_for_sentences(words_list, tags_list)
    se_format_text = build_se_format_for_sentences(words_list, tags_list)
    return render(request, 'tagger/ner_tagger_result.html',
                  {'original_text': text,
                   'conll_format_text': conll_format_text,
                   'se_format_text': se_format_text,
                   'html_format_text': html_format_text,
                   'labels': __labels__,
                   'labels_data_for_js': json.dumps(__labels__), })
