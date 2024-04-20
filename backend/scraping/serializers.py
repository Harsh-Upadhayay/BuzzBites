from rest_framework import serializers
from .models import(
    Meme,
    NewsArticle,
    MatchReport
)

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = '__all__'

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'

class MatchReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchReport
        fields = '__all__'