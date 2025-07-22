from django.db import models
from django.urls import reverse

from webapp.models.base_create_update import BaseCreateUpdateModel


class Comment(BaseCreateUpdateModel):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')

    def __str__(self):
        return self.text[:20]

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"

    def get_absolute_url(self):
        return reverse("webapp:article-detail", kwargs={"pk": self.article_id})