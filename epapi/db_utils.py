from django.db import connection


def get_categories():
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT collection, COUNT(*) '
                       'FROM prod.articles '
                       'GROUP BY collection')
        rows = cursor.fetchall()
    return rows


def get_articles(query=None, category=None):
    where = ''
    if query is not None and category is not None:
        where += 'WHERE lower(title) LIKE \'%{}%\' AND collection = \'{}\' '.format(query.lower(), category)
    elif query is not None:
        where += 'WHERE lower(title) LIKE \'%{}%\' '.format(query.lower())
    elif category is not None:
        where += 'WHERE collection = \'{}\' '.format(category)

    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM prod.articles ' + where)
        total = cursor.fetchone()[0]
    print(total)    

    sql = 'SELECT id, title, collection, url, doi FROM prod.articles '
    sql += where
    sql += 'LIMIT 20'
    print(sql)
    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    data = []
    for row in rows:
        authors = get_authors(row[0])
        data.append(list(row) + [authors])
    return total, data


def get_authors(article):
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT a.name '
                       'FROM prod.authors AS a INNER JOIN prod.article_authors AS aa '
                       'ON a.id=aa.author '
                       'WHERE aa.article=\'{}\''.format(article))
        rows = cursor.fetchall()
    return ', '.join([r[0] for r in rows])
