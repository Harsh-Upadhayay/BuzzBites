from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from scraping.models import (
    Meme,
    NewsArticle,
)
from scraping.serializers import (
    MemeSerializer,
    NewsArticleSerializer
)





class MemeListPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsListPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class MemeListAPIView(generics.ListAPIView):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']
    pagination_class = MemeListPagination
    filterset_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class NewsListAPIView(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = '__all__'
    ordering = ['-published_at']
    pagination_class = NewsListPagination
    filterset_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(summary__isnull=False)
        return queryset

class NewsSummaryGeneratorListAPIView(APIView):
    def get(self, request):
        news_articles = NewsArticle.objects.filter(summary__isnull = True)
        serializer = NewsArticleSerializer(news_articles, many=True)
        return Response(serializer.data)


class NewsSummaryGeneratorDetail(APIView):
    def get_object(self, pk):
        try:
            return NewsArticle.objects.get(pk=pk)
        except NewsArticle.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        news_article = self.get_object(pk)
        serializer = NewsArticleSerializer(news_article)
        return Response(serializer.data)

    def put(self, request, pk):
        news_article = self.get_object(pk)
        serializer = NewsArticleSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)