from django.db.models.base import Model
from movies.serializers import (
    MovieListSerializer, MovieSerializer,
    ReviewListSerializer, CommentListSerializer
    )
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Movie, Review, Comment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from .tmdb import URLMaker
import requests
from django.contrib.auth import get_user_model
from django.conf import settings


@api_view(['GET'])
def index(request):

    maker = URLMaker(settings.TMDB_KEY)
    movies = Movie.objects.all()
    movie_length = len(movies) // 10
    is_empty = False
    
    if not movie_length:
        is_empty = True

    # 길이의 다음 페이지 받아오기
    for page in range(movie_length + 1, movie_length + 2):

        url = maker.get_url(page=page)  
        res = requests.get(url).json() 
        movie_list = res.get('results')
        
        for movie in movie_list:
            title = movie['title']
            overview = movie['overview']
            movie_id = movie['id']

            if 'release_date' in movie.keys():
                if movie['release_date']:
                    release_date = movie['release_date']
                else:
                    continue
            else:
                continue
            
            if 'poster_path' in movie.keys():
                if movie['poster_path']:
                    poster_path = movie['poster_path']
                else:
                    continue
            else:
                continue

            
            film = Movie(
                title = title,
                overview = overview,
                release_date = release_date,
                poster_path = poster_path,
                movie_id = movie_id,
            )

           
            if Movie.objects.filter(title=film.title, overview=film.overview).exists():
                break
            else:
                film.save()

    if is_empty:
        return Response(status=201)

    movies = Movie.objects.order_by('pk')
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    serializer = MovieListSerializer(movies, many=True)
    
    return Response(serializer.data, status=201)
        

@api_view(['GET'])
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviewList = movie.review_set.order_by('pk')

    movie_serializer = MovieSerializer(movie)
    review_serializer = ReviewListSerializer(reviewList, many=True)

    serializer = {
        'movie': movie_serializer.data,
        'reviews': review_serializer.data,
    }
 
    return Response(serializer, status=201)


@api_view(['GET', 'POST'])
def review_create(request, movie_pk):
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=201)  
    else: 
        review = movie.review_set.all()
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=201)


@api_view(['PUT', 'DELETE'])
def review_detail(request, movie_pk, review_pk):

    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "DELETE":
        review.delete()
        return Response(status=200)
    else:
        serializer = ReviewListSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=201)


@api_view(['GET','POST'])
def comment(request, movie_pk, review_pk):
    
    review = get_object_or_404(Review, pk=review_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        serializer = CommentListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, review=review)
            return Response(serializer.data, status=201) 

    else: 
        comments = review.comment_set.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=200)


@api_view(['PUT', 'DELETE'])
def comment_detail(request, movie_pk, review_pk, comment_pk):

    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "DELETE":
        comment.delete()
        return Response(status=200)
    else:
        serializer = CommentListSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, review=review)
            return Response(serializer.data, status=201)


@api_view(['GET'])
def recommend(request):

    movies = Movie.objects.all()

    serializer = MovieListSerializer(movies, many=True)
    
    return Response(serializer.data, status=201)


@api_view(['GET'])
def recommended(request):

    movies = Movie.objects.all()
   
    serializer = MovieListSerializer(movies, many=True)
    
    return Response(serializer.data, status=201)