from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create tables'

    def handle(self, *args, **options):
        self.stdout.write('Creating tables...')
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                  id INT(11) AUTO_INCREMENT,
                  source TEXT NOT NULL,
                  source_id INT(11) NOT NULL,
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
                CREATE INDEX idx_articles_source_id ON articles(source_id)
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS authors (
                  id INT(11) AUTO_INCREMENT,
                  source TEXT NOT NULL,
                  source_id INT(11) NOT NULL,
                  name TEXT NOT NULL,
                  PRIMARY KEY (id)
                ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS article_authors (
                  id INT(11) AUTO_INCREMENT,
                  article_id INT NOT NULL,
                  author_id INT NOT NULL,
                  PRIMARY KEY (id),
                  FOREIGN KEY (article_id) REFERENCES articles(id),
                  FOREIGN KEY (author_id) REFERENCES authors(id)
                ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
            ''')
        self.stdout.write('Tables created')
