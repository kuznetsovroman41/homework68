from django.db import models

from webapp.models.base_create_update import BaseCreateUpdateModel


class Tag(BaseCreateUpdateModel):
    title = models.CharField(max_length=50, verbose_name='Название', null=False, blank=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тэг'
        verbose_name_plural = "Тэги"
