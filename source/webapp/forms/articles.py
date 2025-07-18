from django import forms
from django.core.exceptions import ValidationError
from webapp.forms.base_form import BaseForm
from webapp.models import Article


class ArticleForm(BaseForm):

    class Meta:
        model = Article
        fields = ('title', 'author', 'content', 'status', 'tags',)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long")
        return title

    def clean(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        if title and content and title == content:
            raise ValidationError("Название и контент не могут быть одинаковыми")
        return self.cleaned_data
