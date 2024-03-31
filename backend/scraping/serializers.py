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
    class Meta:
        model = None


class CricbuzzNewsSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        model = CricbuzzNews
        fields = '__all__'

class HindustanTimesNewsSerializer(NewsSerializer):
    class Meta(NewsSerializer.Meta):
        model = HindustanTimesNews
        fields = '__all__'