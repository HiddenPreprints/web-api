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


def to_id(v):
    return 'biorxiv_' + str(v)


class Command(BaseCommand):
    help = 'Import Biorxiv data'

    def handle(self, *args, **options):
        self.stdout.write('Importing Biorxiv data...')

        try:
            biorxiv_conn = get_biorxiv_conn()

            self.stdout.write('Importing authors...')
            with connection.cursor() as cursor:
                for row in get_authors(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO authors(id, source, name)
                        VALUES (%s, 'biorxiv', %s)
                        ON DUPLICATE KEY UPDATE name=VALUES(name)
                    ''', [to_id(row[0]), row[1]])

            self.stdout.write('Importing articles...')
            with connection.cursor() as cursor:
                for row in get_articles(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO articles(id, source, url, title, abstract,
                                             doi, category, posted_date)
                        VALUES (%s, 'biorxiv', %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE url=VALUES(url),
                            title=VALUES(title), abstract=VALUES(abstract),
                            doi=VALUES(doi), category=VALUES(category),
                            posted_date=VALUES(posted_date)
                    ''', [to_id(row[0])] + list(row[1:]))

            self.stdout.write('Importing article_authors...')
            with connection.cursor() as cursor:
                for row in get_article_authors(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO article_authors(article_id, author_id)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE article_id=VALUES(article_id)
                    ''', [to_id(row[0]), to_id(row[1])])
        finally:
            biorxiv_conn.close()
        self.stdout.write('Biorxiv data imported')
