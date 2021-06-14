from rest_framework import serializers
from .models import Movie, Review, Comment

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
        

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'release_date', 'poster_path', 'movie_id')
        

class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user_id')


class CommentListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'movie', 'user_id')
