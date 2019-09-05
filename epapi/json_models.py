import re

from rest_framework import serializers


class Category(object):
    def __init__(self, data):
        self.key = data[0]
        self.name = re.sub('-', ' ', str(data[0])).title()
        self.total = data[1]


class CategorySerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    total = serializers.IntegerField()


class Article(object):
    def __init__(self, data):
        self.id = data[0]
        self.title = data[1]
        self.category = data[2]
        self.url = data[3]
        self.doi = data[4]
        self.authors = data[5]


class Articles(object):
    def __init__(self, data):
        self.total = data[0]
        self.articles = [Article(a) for a in data[1]]
    

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField()
    url = serializers.CharField()
    doi = serializers.CharField()
    authors = serializers.CharField()


class ArticlesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    articles = ArticleSerializer(many=True)
