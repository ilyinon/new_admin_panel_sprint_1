import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('added_entry'), auto_now_add=True)
    modified = models.DateTimeField(_('updated_entry'), auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

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
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'), blank=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):

    class RoleType(models.TextChoices):
        DIRECTOR = "DIRECTOR", (_('director'))
        ACTOR = "ACTOR", (_('actor'))
        PRODUCER = "PRODUCER", (_('producer'))
        ANIMATOR = "ANIMATOR", (_('animator'))
        AUDIO_ENGINEER = "AUDIO_ENGINEER", (_('audio_engineer'))

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'),
                            max_length=20,
                            choices=RoleType.choices,
                            default=RoleType.ACTOR,
                            )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
