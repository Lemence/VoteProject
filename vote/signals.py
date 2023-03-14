import os
import zipfile
from urllib import request
import openpyxl
import psycopg2
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def first_migrate(sender, **kwargs):
    from vote.models import Votes
    Votes.objects.all().delete()

    url = "https://op.mos.ru/EHDWSREST/catalog/export/get?id=1494876"
    filename = 'vote/download/votes.zip'

    request.urlretrieve(url, filename)

    with zipfile.ZipFile('vote/download/votes.zip', "r") as zip_ref:
        zip_ref.extractall('vote/download/')

    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='db', port='5432')
    cursor = conn.cursor()
    extension = ".xlsx"
    for filename in os.listdir("vote/download"):
        if filename.endswith(extension):
            workbook = openpyxl.load_workbook(f"vote/download/{filename}")
            worksheet = workbook.active

            for row in worksheet.iter_rows():
                data = []
                for cell in row:
                    data.append(cell.value)
                cursor.execute(
                    'INSERT INTO vote_votes (global_id, votingname, linktoresults, votingname_en, linktoresults_en) VALUES (%s, %s, %s, %s, %s)',
                    data)

    conn.commit()
    cursor.close()
    conn.close()

    folder_path = 'vote/download'
    for item in os.scandir(folder_path):
        os.unlink(item.path)