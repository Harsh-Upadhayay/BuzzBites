from django.urls import path
from .views import MemeListAPIView

urlpatterns = [
    path('memes/', MemeListAPIView.as_view(), name='meme-list'),
]
