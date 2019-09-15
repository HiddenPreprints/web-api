from rest_framework import viewsets, routers
from rest_framework.response import Response

from .db_utils import get_categories, get_articles
from .json_models import CategorySerializer, ArticlesSerializer


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = get_categories()
        categories.sort(key=lambda c: c.total, reverse=True)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        params = request.GET.dict()
        query = params.get('query')
        category = params.get('category')
        articles = get_articles(query=query, category=category)

        serializer = ArticlesSerializer(articles)
        return Response(serializer.data)


categories_router = routers.DefaultRouter()
categories_router.register(r'categories', CategoryViewSet, basename='category')
categories_router.register(r'articles', ArticleViewSet, basename='article')
