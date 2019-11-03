from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create tables'

    def handle(self, *args, **options):
        self.stdout.write('Creating tables...')
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                  id VARCHAR(200) NOT NULL,
                  source VARCHAR(200) NOT NULL,
                  doi TEXT,
                  url TEXT,
                  title TEXT NOT NULL,
                  abstract TEXT,
                  category TEXT,
                  posted_date DATE,
                  shadow_index FLOAT,
                  PRIMARY KEY (id)
                ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS authors (
                  id VARCHAR(200) NOT NULL,
                  source VARCHAR(200) NOT NULL,
                  name TEXT NOT NULL,
                  PRIMARY KEY (id)
                ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS article_authors (
                  id INT(11) AUTO_INCREMENT,
                  article_id VARCHAR(200) NOT NULL,
                  author_id VARCHAR(200) NOT NULL,
                  PRIMARY KEY (id),
                  FOREIGN KEY (article_id) REFERENCES articles(id),
                  FOREIGN KEY (author_id) REFERENCES authors(id),
                  UNIQUE (article_id, author_id)
                ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
            ''')
        self.stdout.write('Tables created')
