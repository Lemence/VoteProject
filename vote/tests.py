import os
from unittest.mock import patch
from urllib import request
import psycopg2
from django.test import TestCase
from vote.models import Votes
from vote.tasks import migrate_votes


class MigrateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = "https://op.mos.ru/EHDWSREST/catalog/export/get?id=1494876"
        cls.filename = 'vote/download/votes.zip'

    def test_download_and_clear(self):
        request.urlretrieve(self.url, self.filename)
        self.assertTrue(os.path.exists(self.filename))
        folder_path = 'vote/download'
        for item in os.scandir(folder_path):
            os.unlink(item.path)
        files = os.listdir('vote/download')
        self.assertEqual(len(files), 0)

    def test_create_votes(self):
        migrate_votes()
        votes = Votes.objects.all()
        self.assertGreater(len(votes), 0)
        for vote in votes:
            self.assertIsInstance(vote.global_id, str)
            self.assertIsInstance(vote.votingname, str)
            self.assertIsInstance(vote.linktoresults, str)
            self.assertIsInstance(vote.votingname_en, (str, type(None)))
            self.assertIsInstance(vote.linktoresults_en, (str, type(None)))

    def test_database_connection(self):
        with self.assertRaises(psycopg2.Error):
            with patch('vote.tasks.psycopg2.connect') as mock_conn:
                mock_conn.side_effect = psycopg2.Error()
                migrate_votes()
