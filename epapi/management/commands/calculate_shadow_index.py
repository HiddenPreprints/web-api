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


def get_shadow_index(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT id, shadow_index
            FROM prod.enhanced
        ''')
        for row in cursor:
            yield row


class Command(BaseCommand):
    help = 'Calculate shadow index'

    def handle(self, *args, **options):
        self.stdout.write('Calculating Shadow Index...')
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TEMPORARY TABLE s_i_tmp (
                  id INT(11) NOT NULL,
                  shadow_index FLOAT,
                  PRIMARY KEY (id)
            )''')

        try:
            biorxiv_conn = get_biorxiv_conn()

            with connection.cursor() as cursor:
                for row in get_shadow_index(biorxiv_conn):
                    cursor.execute('''
                        INSERT INTO s_i_tmp
                        VALUES(%s, %s)
                    ''', row)
        finally:
            biorxiv_conn.close()
        self.stdout.write('Temporary Shadow Index table created...')

        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE articles a
                INNER JOIN s_i_tmp b ON a.source_id = b.id
                SET a.shadow_index = b.shadow_index
            ''')
        self.stdout.write('Shadow Index calculated')
