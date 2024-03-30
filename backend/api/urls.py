from django.urls import path
from .views import (
    MemeListAPIView,
    NewsListAPIView
)

urlpatterns = [
    path('memes/', MemeListAPIView.as_view(), name='meme-list'),
    path('news/', NewsListAPIView.as_view(), name='news-list'),
]
