from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class TaggedTextForm(forms.Form):
    input_text = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'tagged_text', "readonly":True, 'class': 'form-control'}))
    post_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'id': 'post_id_in_form', "readonly":True, 'class': 'form-control'}))
