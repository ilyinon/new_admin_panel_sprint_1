import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

# Create your models here.
class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры' 

    def __str__(self):
        return self.name 

class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkType(models.TextChoices):
        MOVIE = "MV", ("movie")
        TV_SHOW = "TV", ("tv_show")

    title = models.CharField(_('title'), max_length=255)
    type = models.CharField(
        max_length=2,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    description = models.TextField(_('description'), blank=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    creation_date = models.DateTimeField()


    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"filmwork"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения' 

    def __str__(self):
        return self.title 
    
class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work" 

class Gender(models.TextChoices):
    MALE = 'male', ('male')
    FEMALE = 'female', ('female')

# class Person(UUIDMixin, TimeStampedMixin):
#     gender = models.TextField(('gender'), choices=Gender.choices, null=True) 

# class PersonFilmwork(UUIDMixin):
#     pass
    # film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    # person = models.ForeignKey('Person', on_delete=models.CASCADE)
    # role = models.TextField('role')
    # created = models.DateTimeField(auto_now_add=True) 
    # profession = models.TextField(_('profession'), choices=RoleType.choices, null=True)
    # role = models.TextField(_('role'), null=True) 




#     operations = [
#     migrations.RunSQL(
#         sql="""
#             ALTER TABLE "content"."genre_film_work" 
#             ADD CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq" 
#             UNIQUE ("film_work_id", "genre_id");
#         """,
#         reverse_sql='ALTER TABLE "content"."genre_film_work" DROP CONSTRAINT genre_film_work_film_work_id_genre_id_uniq',
#     )
# ] 