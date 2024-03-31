from rest_framework import serializers
from .models import(
    Meme,
    CricbuzzNews,
    HindustanTimesNews
)

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    # news_id = serializers.CharField()
    # news_url = serializers.CharField()
    # news_title = serializers.CharField()
    # news_description = serializers.CharField()
    # news_summary = serializers.CharField()
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()
    class Meta:
        model = None  # Setting to None as we will define it dynamically based on the queryset


class CricbuzzNewsSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        model = CricbuzzNews
        fields = '__all__'

class HindustanTimesNewsSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        model = HindustanTimesNews
        fields = '__all__'