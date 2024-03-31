from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from scraping.models import (
    Meme,
    HindustanTimesNews,
    CricbuzzNews
)
from scraping.serializers import (
    MemeSerializer,
    NewsSerializer,
    HindustanTimesNewsSerializer,
    CricbuzzNewsSerializer
)
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class MemeListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsListPagination(PageNumberPagination):
    page_size = 10
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
    serializer_class = None
    pagination_class = NewsListPagination

    def get_serializer_class(self):
        queryset = self.get_queryset()
        if queryset and isinstance(queryset[0], HindustanTimesNews):
            return HindustanTimesNewsSerializer
        elif queryset and isinstance(queryset[0], CricbuzzNews):
            return CricbuzzNewsSerializer
        return NewsSerializer

    def get_queryset(self):
        hindustan_news = HindustanTimesNews.objects.all()
        cricbuzz_news = CricbuzzNews.objects.all()
        queryset = list(hindustan_news) + list(cricbuzz_news)
        queryset.sort(key=lambda x: x.created_at, reverse=True)
        return queryset
