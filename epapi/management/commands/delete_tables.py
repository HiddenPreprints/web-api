from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete tables'

    def handle(self, *args, **options):
        self.stdout.write('Deleting tables...')
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS article_authors')
            cursor.execute('DROP TABLE IF EXISTS articles')
            cursor.execute('DROP TABLE IF EXISTS authors')
        self.stdout.write('Tables deleted')
