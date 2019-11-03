import re

from rest_framework import serializers


class Category(object):
    def __init__(self, key, total):
        self.key = key
        self.name = re.sub('-', ' ', str(key)).title()
        self.total = total


class CategorySerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    total = serializers.IntegerField()


class Article(object):
    def __init__(self, id, source, title, category, url, doi, posted, authors,
                 shadow_index):
        self.id = id
        self.source = source
        self.title = title
        self.authors = authors
        self.posted = posted
        self.category = category
        self.url = url
        self.doi = doi
        self.shadow_index = round(shadow_index, 3)


class Articles(object):
    def __init__(self, total, articles):
        self.total = total
        self.articles = articles


class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField()
    source = serializers.CharField()
    title = serializers.CharField()
    authors = serializers.CharField()
    posted = serializers.DateField()
    category = serializers.CharField()
    url = serializers.CharField()
    doi = serializers.CharField()
    shadow_index = serializers.FloatField()


class ArticlesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    articles = ArticleSerializer(many=True)
