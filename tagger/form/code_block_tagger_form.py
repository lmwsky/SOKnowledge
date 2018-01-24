from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CodeBlockTaggerForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea(attrs={'id': 'input_text','class':'form-control'}))

    def clean_input_text(self):
        data = self.cleaned_data['input_text']
        data = data.strip()
        # Check text is not null.
        if not data:
            raise ValidationError(_('the input must not be empty'))

        # Remember to always return the cleaned data.
        return data
