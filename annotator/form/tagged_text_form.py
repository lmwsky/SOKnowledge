from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class TaggedTextForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea(attrs={'id': 'tagged_text'}))
    post_id = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'post_id_in_form'}))

    def clean_input_text(self):
        data = self.cleaned_data['input_text']
        data = data.strip()
        # Check text is not null.
        if not data:
            raise ValidationError(_('the input must not be empty'))

        # Remember to always return the cleaned data.
        return data

    def clean_post_id(self):
        post_id = self.cleaned_data['post_id']
        data = post_id
        # Check text is not null.
        if not data:
            raise ValidationError(_('the input must not be empty'))

        # Remember to always return the cleaned data.
        return data
