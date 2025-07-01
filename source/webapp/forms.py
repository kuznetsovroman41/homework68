from django import forms
from django.forms import widgets

from webapp.models import statuses


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        label='Title',
        widget=widgets.Input(attrs={"class": "form-control"}),
        error_messages={'required': 'Please enter title'},

    )
    author = forms.CharField(max_length=5, required=True, label='Author', widget=widgets.Input(attrs={"class": "form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": "20", "rows": "5", "class": "form-control"}), required=True, label='Content')
    status = forms.ChoiceField(choices=statuses, widget=widgets.Select(attrs={"class": "form-control"}),)
