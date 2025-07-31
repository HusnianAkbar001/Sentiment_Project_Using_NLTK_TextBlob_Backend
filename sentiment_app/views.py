from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from textblob import TextBlob
from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer

class AnalyzeSentimentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        input_text = request.data.get('input_text', '')
        
        if not input_text.strip():
            return Response(
                {'error': 'Input text is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Analyze sentiment using TextBlob
            blob = TextBlob(input_text)
            polarity_score = blob.sentiment.polarity
            
            # Determine sentiment based on polarity
            if polarity_score > 0.1:
                sentiment = 'positive'
            elif polarity_score < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Save to database
            sentiment_analysis = SentimentAnalysis.objects.create(
                user=request.user,
                input_text=input_text,
                sentiment=sentiment,
                polarity_score=polarity_score
            )
            
            # Return result
            return Response({
                'id': sentiment_analysis.id,
                'input_text': input_text,
                'sentiment': sentiment,
                'polarity_score': polarity_score,
                'created_at': sentiment_analysis.created_at
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Analysis failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SentimentHistoryView(generics.ListAPIView):
    serializer_class = SentimentAnalysisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        # Return all sentiment analyses (as per your requirement)
        return SentimentAnalysis.objects.all().order_by('-created_at')

class DeleteSentimentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        # Only admin can delete
        if request.user.role != 'admin':
            return Response(
                {'error': 'Only admin users can delete sentiment analyses'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        sentiment_analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        sentiment_analysis.delete()
        
        return Response(
            {'message': 'Sentiment analysis deleted successfully'}, 
            status=status.HTTP_200_OK
        )