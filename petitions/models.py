from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Petition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    votes = models.ManyToManyField(User, related_name='petition_votes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return self.name
