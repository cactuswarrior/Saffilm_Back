from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/reviews/', views.review_create, name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/comments/', views.comment, name="comment"),
    path('<int:movie_pk>/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('recommend/', views.recommend, name='recommend'),
    path('recommended/', views.recommended, name='recommended'),
]
