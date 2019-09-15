from django.db import connection

from .json_models import Category, Article, Articles


def get_categories():
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT collection, COUNT(*) '
                       'FROM prod.enhanced '
                       'GROUP BY collection')
        rows = cursor.fetchall()
    return [Category(row[0], row[1]) for row in rows]


def get_articles(query=None, category=None):
    where_clauses = ['shadow_index IS NOT null']
    params = []
    if query is not None:
        where_clauses.append('lower(title) LIKE %s')
        params.append('%' + query.lower() + '%')
    if category is not None:
        where_clauses.append('collection = %s')
        params.append(category)
    where = 'WHERE ' + ' AND '.join(where_clauses)

    total = 0
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM prod.enhanced ' + where, params)
        total = cursor.fetchone()[0]

    sql = 'SELECT id, title, collection, url, doi, shadow_index '
    sql += 'FROM prod.enhanced '
    sql += where
    sql += ' ORDER BY shadow_index DESC LIMIT 20'
    print(sql)

    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    data = [Article(row[0], row[1], row[2], row[3], row[4],
                    get_authors(row[0]), row[5])
            for row in rows]
    return Articles(total, data)


def get_authors(article):
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT a.name '
                       'FROM prod.authors AS a '
                       'INNER JOIN prod.article_authors AS aa '
                       'ON a.id=aa.author '
                       'WHERE aa.article=\'{}\''.format(article))
        rows = cursor.fetchall()
    return ', '.join([r[0] for r in rows])
