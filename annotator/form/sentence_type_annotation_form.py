from django.forms import ModelForm, forms, ModelChoiceField, CharField, Select, Textarea

from annotator.models import SentenceTypeAnnotation
from annotator.annotator_util import __sentence_type_list__


class SentenceTypeAnnotationForm(ModelForm):
    sentence_type = ModelChoiceField(queryset=__sentence_type_list__, widget=Select(attrs={'class': 'form-control'}))
    annotation_text = CharField(
        widget=Textarea(attrs={'id': 'tagged_text', 'rows': "3", "readonly": True, 'class': 'form-control sentence'})
        )

    class Meta:
        model = SentenceTypeAnnotation
        fields = ['annotation_text', 'sentence_type']
