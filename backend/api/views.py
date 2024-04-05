from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from scraping.models import (
    Meme,
    NewsArticle,
)
from scraping.serializers import (
    MemeSerializer,
    NewsArticleSerializer
)
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


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
    ordering = ['-created_at']  # Default ordering by created_at field
    pagination_class = MemeListPagination
    filterset_fields = '__all__'  # Enable filtering based on all fields

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class NewsListAPIView(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = '__all__'
    ordering = ['-updated_at']  # Default ordering by created_at field
    pagination_class = NewsListPagination
    filterset_fields = '__all__'  # Enable filtering based on all fields

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
