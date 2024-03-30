from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from scraping.models import Meme
from scraping.serializers import MemeSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class MemeListPagination(PageNumberPagination):
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
