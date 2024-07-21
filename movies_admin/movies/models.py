from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .mixins import TimeStampedMixin, UUIDMixin

class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        managed = False
        db_table = "content\".\"genre"
        verbose_name = (_('genre'))
        verbose_name_plural = (_('genres'))
        indexes = [
            models.Index(fields=['name'], name='genre_name_idx'),
        ]

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkType(models.TextChoices):
        MOVIE = "MV", (_('movie'))
        TV_SHOW = "TV", (_('tv_show'))

    title = models.CharField(_('title'), max_length=255)
    type = models.CharField(_('type'),
                            max_length=2,
                            choices=FilmworkType.choices,
                            default=FilmworkType.MOVIE,
                            )
    description = models.TextField(_('description'), blank=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    creation_date = models.DateTimeField(_('published'))

    class Meta:
        managed = False
        db_table = "content\".\"film_work"
        verbose_name = (_('filmwork'))
        verbose_name_plural = (_('filmworks'))
        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ]

    def __str__(self):
        return self.title


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'), blank=False)

    class Meta:
        managed = False
        db_table = "content\".\"person"
        verbose_name = (_('person'))
        verbose_name_plural = (_('persons'))

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=(_('filmwork')))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=(_('genre')))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "content\".\"genre_film_work"
        verbose_name = (_('Filmwork genre'))
        verbose_name_plural = (_('Filmwork genres'))
        unique_together = ['film_work_id', 'genre_id']
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id' ], name='film_work_genre_idx'),
            models.Index(fields=['film_work_id'], name='genre_film_work_film_work_idx')
        ]

class PersonFilmwork(UUIDMixin):

    class RoleType(models.TextChoices):
        DIRECTOR = "direcotr", (_('director'))
        ACTOR = "actor", (_('actor'))
        PRODUCER = "writer", (_('writer'))

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=(_('filmwork')))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=(_('person')))
    role = models.CharField(_('role'),
                            max_length=20,
                            choices=RoleType.choices,
                            default=RoleType.ACTOR,
                            )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "content\".\"person_film_work"
        verbose_name = (_('Role person in filmwork'))
        verbose_name_plural = (_('Roles person in filmwork'))
        unique_together = ['film_work_id', 'person_id', 'role']
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role' ], name='film_work_person_idx'),
        ]
