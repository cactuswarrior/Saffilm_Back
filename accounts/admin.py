from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from movies.models import Movie


class MovieAdmin(admin.ModelAdmin):

    list_display = ('title', 'overview', 'release_date', 'poster_path')


admin.site.register(User, UserAdmin)
admin.site.register(Movie, MovieAdmin)

