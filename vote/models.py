from django.db import models
import openpyxl
import psycopg2
import time


class Votes(models.Model):
    global_id = models.CharField(max_length=20, verbose_name='Идентификатор')
    votingname = models.CharField(max_length=256, verbose_name='Название голосования')
    linktoresults = models.URLField(verbose_name='Ссылка на результаты')
    votingname_en = models.CharField(max_length=256, verbose_name='Англоязычное название', null=True)
    linktoresults_en = models.URLField(verbose_name='Англоязычные результаты', null=True)

    def __str__(self):
        return self.votingname

    class Meta:
        verbose_name_plural= 'Голоса'




