from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SentimentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    sentiment = models.CharField(max_length=20)
    polarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.sentiment}'
