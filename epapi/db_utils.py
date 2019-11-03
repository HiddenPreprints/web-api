from django.db import connection

from .json_models import Category, Article, Articles


def get_categories():
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT category, COUNT(*)
            FROM articles
            GROUP BY category
        ''')
        rows = cursor.fetchall()
    return [Category(row[0], row[1]) for row in rows]


def get_articles(query=None, category=None, posted_since=None):
    where_clauses = ['shadow_index IS NOT null']
    params = []
    if query is not None:
        where_clauses.append(
            '(lower(title) LIKE %s OR lower(abstract) LIKE %s)')
        params.extend(['%' + query.lower() + '%'] * 2)
    if category is not None:
        where_clauses.append('category = %s')
        params.append(category)
    if posted_since is not None:
        where_clauses.append('posted_date >= %s')
        params.append(posted_since)
    where = 'WHERE ' + ' AND '.join(where_clauses)

    total = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM articles ' + where, params)
        total = cursor.fetchone()[0]

    sql = 'SELECT id, source, title, category, url, doi, posted_date, ' + \
        'shadow_index '
    sql += 'FROM articles '
    sql += where
    sql += ' ORDER BY shadow_index DESC LIMIT 20'

    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    data = [Article(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                    get_authors(row[0]), row[7])
            for row in rows]
    return Articles(total, data)


def get_authors(article):
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT a.name, aa.id
            FROM authors AS a
            INNER JOIN article_authors AS aa ON a.id=aa.author_id
            WHERE aa.article_id=%s
            ORDER BY aa.id
        ''', [article])
        rows = cursor.fetchall()
    return ', '.join([r[0] for r in rows])
