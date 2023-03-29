import zipfile
import openpyxl
import psycopg2
from celery import shared_task
from urllib import request
import os
from django.db import transaction
from django.apps import apps
from .models import Votes

@shared_task()
@transaction.atomic
def migrate_votes():
    Votes.objects.all().delete()

    url = "https://op.mos.ru/EHDWSREST/catalog/export/get?id=1494876" # Скачиваем архиф с данными
    filename = 'vote/download/votes.zip'

    request.urlretrieve(url, filename)

    with zipfile.ZipFile('vote/download/votes.zip', "r") as zip_ref: # Разорхивируем
        zip_ref.extractall('vote/download/')

    extension = ".xlsx"
    for filename in os.listdir("vote/download"): # Делим файл
        if filename.endswith(extension):
            workbook = openpyxl.load_workbook(f"vote/download/{filename}")
            worksheet = workbook.active

            for row in worksheet.iter_rows():  # Заливаем данные с файла
                data = []
                for cell in row:
                    data.append(cell.value)
                if data[0] == 'global_id':
                    pass
                else:
                    Votes.objects.create(global_id=data[0],
                                         votingname=data[1],
                                         linktoresults=data[2],
                                         votingname_en=data[3],
                                         linktoresults_en=data[4])


    folder_path = 'vote/download' # Очистка папки от ненужных файлов
    for item in os.scandir(folder_path):
        os.unlink(item.path)

