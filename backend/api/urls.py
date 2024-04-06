from django.urls import path
from .views import (
    MemeListAPIView,
    NewsListAPIView,
    NewsSummaryGeneratorListAPIView,
    NewsSummaryGeneratorDetail,
)

urlpatterns = [
    path('memes/', MemeListAPIView.as_view(), name='meme-list'),
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('generate-summary/', NewsSummaryGeneratorListAPIView.as_view(), name='empty-summary-news-list'),
    path('generate-summary/<int:pk>/', NewsSummaryGeneratorDetail.as_view(), name='empty-summary-news-detail'),
]
