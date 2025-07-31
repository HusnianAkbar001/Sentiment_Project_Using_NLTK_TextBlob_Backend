from rest_framework import serializers
from .models import SentimentAnalysis
from users.serializers import UserSerializer

class SentimentAnalysisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SentimentAnalysis
        fields = ['id', 'user', 'input_text', 'sentiment', 'polarity_score', 'created_at']
        read_only_fields = ['user', 'sentiment', 'polarity_score', 'created_at']