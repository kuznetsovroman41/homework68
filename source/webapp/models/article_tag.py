from django.db import models

from webapp.models.base_create_update import BaseCreateUpdateModel


class ArticleTag(BaseCreateUpdateModel):
    article = models.ForeignKey('webapp.Article', related_name='articles_tags', on_delete=models.CASCADE,)
    tag = models.ForeignKey('webapp.Tag', related_name='tags_articles', on_delete=models.CASCADE,)