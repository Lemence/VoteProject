import os
import zipfile
from urllib import request
import openpyxl
import psycopg2
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def first_migrate(sender, **kwargs):
    Votes = apps.get_model('vote', 'Votes')  # импортируем модель Votes уже после загрузки приложения
    Votes.objects.all().delete()

    url = "https://op.mos.ru/EHDWSREST/catalog/export/get?id=1494876"  # Скачиваем архиф с данными
    filename = 'vote/download/votes.zip'

    request.urlretrieve(url, filename)

    with zipfile.ZipFile('vote/download/votes.zip', "r") as zip_ref:  # Разорхивируем
        zip_ref.extractall('vote/download/')

    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='db', port='5432')
    cursor = conn.cursor()
    extension = ".xlsx"
    for filename in os.listdir("vote/download"):  # Делим файл
        if filename.endswith(extension):
            workbook = openpyxl.load_workbook(f"vote/download/{filename}")
            worksheet = workbook.active

            for row in worksheet.iter_rows(): # Заливаем данные с файла
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

    conn.commit()
    cursor.close()
    conn.close()

    folder_path = 'vote/download'  # Очистка папки от ненужных файлов
    for item in os.scandir(folder_path):
        os.unlink(item.path)