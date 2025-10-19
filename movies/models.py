from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    
    def average_rating(self):
        from django.db.models import Avg
        avg_rating = self.rating_set.aggregate(Avg('stars'))['stars__avg']
        return round(avg_rating, 1) if avg_rating else None
    
    def rating_count(self):
        return self.rating_set.count()
    
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'user')  # One rating per user per movie
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.name} - {self.stars} stars"