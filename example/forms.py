from django import forms
from .models import example


class StockForm(forms.ModelForm):
    class Meta:
        model = example
        fields = ['ticker'] # fields = ['pub_date', 'headline', 'content', 'reporter']
