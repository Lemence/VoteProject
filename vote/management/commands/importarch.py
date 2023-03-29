from django.core.management.base import BaseCommand
from vote.tasks import migrate_votes


class Command(BaseCommand):
    help = 'Импортирует архив, разархивирует его и загружает в базу'

    def handle(self, *args, **options):
        migrate_votes()




