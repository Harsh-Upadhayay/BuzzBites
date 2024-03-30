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

class CricbuzzNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CricbuzzNews
        fields = '__all__'

class HindustanTimesNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HindustanTimesNews
        fields = '__all__'