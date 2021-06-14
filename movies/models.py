from django.db import models
from django.db.models.fields import BooleanField, DateTimeField
from django.conf import settings


class Movie(models.Model):
    
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    movie_id = models.IntegerField()


class Review(models.Model):
  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=50)
    review_content = models.TextField()
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = BooleanField(default=False)
    is_created = BooleanField(default=False)
    show_comment = BooleanField(default=False)


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = BooleanField(default=False)
