from django.db import connection


def get_categories():
    rows = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT collection, COUNT(*) '
                       'FROM prod.enhanced '
                       'GROUP BY collection')
        rows = cursor.fetchall()
    return rows


def get_articles(query=None, category=None):
    where = 'WHERE shadow_index IS NOT null '
    params = []
    if query is not None and category is not None:
        params = ['%' + query.lower() + '%', category]
        where += 'AND lower(title) LIKE %s AND collection = %s '
    elif query is not None:
        params = ['%' + query.lower() + '%']
        where += 'AND lower(title) LIKE %s '
    elif category is not None:
        params = [category]
        where += 'AND collection = %s '

    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM prod.enhanced ' + where, params)
        total = cursor.fetchone()[0]
    print(total)    

    sql = 'SELECT id, title, collection, url, doi, shadow_index FROM prod.enhanced '
    sql += where
    sql += 'ORDER BY shadow_index DESC LIMIT 20'
    print(sql)
    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
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
