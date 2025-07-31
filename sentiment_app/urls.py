from django.urls import path
from .views import AnalyzeSentimentView, SentimentHistoryView, DeleteSentimentView

urlpatterns = [
    path('analyze/', AnalyzeSentimentView.as_view(), name='analyze-sentiment'),
    path('history/', SentimentHistoryView.as_view(), name='sentiment-history'),
    path('delete/<int:pk>/', DeleteSentimentView.as_view(), name='delete-sentiment'),
]