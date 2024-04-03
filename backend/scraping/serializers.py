from rest_framework import serializers
from .models import(
    Meme,
    NewsArticle,
)

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = '__all__'

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'