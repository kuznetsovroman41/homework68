from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Article


class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs['class'] = 'form-control'

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
