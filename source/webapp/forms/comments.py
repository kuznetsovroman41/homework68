from django import forms

from webapp.forms.base_form import BaseForm
from webapp.models import Comment


class CommentForm(BaseForm):

    class Meta:
        model = Comment
        fields = ('text', 'author',)
