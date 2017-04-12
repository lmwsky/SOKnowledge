import json
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from SOKnowledge.ctr_util.code_block_type_tagger import CodeBlockTypeTagger
from SOKnowledge.data_processor.scripts.nlp_util import sent_word_tokenize_nltk
from SOKnowledge.ner_util.tagger import NERTagger
from SOKnowledge.settings import BASE_DIR
from form.multi_line_text_form import MultiLineTextForm
from SOKnowledge.ner_util.format_util import __labels__, build_conll_format_for_sentences, \
    build_html_format_for_sentences, \
    build_se_format_for_sentences, __code_block_labels__
from tagger.form.code_block_tagger_form import CodeBlockTaggerForm

__is_load_ner_tagger__=True
__is_load_cbr_tagger__=True
__ner_tagger__ = NERTagger()
if __is_load_ner_tagger__:
    __ner_tagger__.load_model(os.path.join(BASE_DIR, 'SOKnowledge/ner_util', 'models/so_for_epochs50_splitwords'))

__code_block_tagger__ = NERTagger()
if __is_load_cbr_tagger__:
    __code_block_tagger__.load_model(os.path.join(BASE_DIR, 'SOKnowledge/ner_util', 'models/large_code_block_tagger'))

__code_block_type_tagger__ = CodeBlockTypeTagger()
#__code_block_type_tagger__.init_model_bays()


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
    text = sent_word_tokenize_nltk(text)
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


def code_block_tagger(request):
    if request.method == 'POST':
        form = CodeBlockTaggerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            return HttpResponseRedirect(reverse('tagger:code_block_tagger_result', args=(text,)))
    else:
        form = CodeBlockTaggerForm()
        return render(request, 'tagger/code_block_tagger_form.html', {'form': form})


def code_block_tagger_result(request, text):
    text = sent_word_tokenize_nltk(text)
    words_list, tags_list = __code_block_tagger__.tag(text)

    conll_format_text = build_conll_format_for_sentences(words_list, tags_list)
    html_format_text = build_html_format_for_sentences(words_list, tags_list)
    se_format_text = build_se_format_for_sentences(words_list, tags_list, __code_block_labels__)
    return render(request, 'tagger/ner_tagger_result.html',
                  {'original_text': text,
                   'conll_format_text': conll_format_text,
                   'se_format_text': se_format_text,
                   'html_format_text': html_format_text,
                   'labels': __code_block_labels__,
                   'labels_data_for_js': json.dumps(__code_block_labels__), })


def code_block_type_tagger(request):
    if request.method == 'POST':
        form = CodeBlockTaggerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['input_text']
            return HttpResponseRedirect(reverse('tagger:code_block_type_tagger_result', args=(text,)))
    else:
        form = CodeBlockTaggerForm()
        return render(request, 'tagger/code_block_type_tagger_form.html', {'form': form})


def code_block_type_tagger_result(request, text):
    print text
    code_block_type_list = __code_block_type_tagger__.tag(text)
    print code_block_type_list

    return render(request, 'tagger/code_block_type_tagger_result.html',
                  {'original_text': text,
                   'labels': __code_block_labels__,
                   'labels_data_for_js': json.dumps(__code_block_labels__),
                   'code_block_type_list': code_block_type_list,
                   })
"""
    text = sent_word_tokenize_nltk(text)

    words_list, tags_list = __code_block_tagger__.tag(text)

    html_format_text = build_html_format_for_sentences(words_list, tags_list)
    se_format_text = build_se_format_for_sentences(words_list, tags_list, __code_block_labels__)

    code_block_type_tagger_input_text = html_format_text.replace("LARGECODE", "code")
    print code_block_type_tagger_input_text
    code_block_type_list = __code_block_type_tagger__.tag(code_block_type_tagger_input_text)
    print code_block_type_list

    return render(request, 'tagger/code_block_type_tagger_result.html',
                  {'original_text': text,
                   'se_format_text': se_format_text,
                   'html_format_text': html_format_text,
                   'labels': __code_block_labels__,
                   'labels_data_for_js': json.dumps(__code_block_labels__),
                   'code_block_type_list': code_block_type_list,
                   })
"""

