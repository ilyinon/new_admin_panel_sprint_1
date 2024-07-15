from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass  

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,) 

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')