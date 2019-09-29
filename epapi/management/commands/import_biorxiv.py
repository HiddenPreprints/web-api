import psycopg2

from epapi.settings import SOURCES

from django.db import connection
from django.core.management.base import BaseCommand


def get_biorxiv_conn():
    DB_CONFIG = SOURCES['biorxiv']
    return psycopg2.connect(user=DB_CONFIG['USER'],
                            password=DB_CONFIG['PASSWORD'],
                            host=DB_CONFIG['HOST'],
                            port=DB_CONFIG['PORT'],
                            database=DB_CONFIG['DATABASE'])


def get_authors(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT id, name
            FROM prod.authors
        ''')
        for row in cursor:
            yield row


def get_articles(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT id, url, title, abstract, doi, collection, posted
            FROM prod.enhanced
        ''')
        for row in cursor:
            yield row


def get_article_authors(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT article, author
            FROM prod.article_authors
        ''')
        for row in cursor:
            yield row


class Command(BaseCommand):
    help = 'Import Biorxiv data'

    def handle(self, *args, **options):
        self.stdout.write('Importing Biorxiv data...')

        try:
            biorxiv_conn = get_biorxiv_conn()

            self.stdout.write('Importing authors...')
            authors = {}
            with connection.cursor() as cursor:
                for row in get_authors(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO authors(source, source_id, name)
                        VALUES ('biorxiv', %s, %s)
                    ''', row)
                    authors[row[0]] = cursor.lastrowid

            self.stdout.write('Importing articles...')
            articles = {}
            with connection.cursor() as cursor:
                for row in get_articles(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO articles(source, source_id, url, title,
                                      abstract, doi, category, posted_date)
                        VALUES ('biorxiv', %s, %s, %s, %s, %s, %s, %s)
                    ''', row)
                    articles[row[0]] = cursor.lastrowid

            self.stdout.write('Importing article_authors...')
            with connection.cursor() as cursor:
                for row in get_article_authors(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO article_authors(article_id, author_id)
                        VALUES (%s, %s)
                    ''', [articles[row[0]], authors[row[1]]])
        finally:
            biorxiv_conn.close()
        self.stdout.write('Biorxiv data imported')
