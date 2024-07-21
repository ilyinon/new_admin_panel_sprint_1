from dataclasses import dataclass
from uuid import UUID
import datetime
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


@dataclass
class User:
    id: UUID
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class Genre:
    id: UUID
    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class FilmWork:
    id: UUID
    title: str
    description: str
    creation_date: datetime.datetime
    certificate: str
    file_path: str
    rating: float
    type: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class GenreFilmWork:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created: datetime.datetime


@dataclass
class PersonFilmWork:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime.datetime


if __name__ == '__main__':
    logging.error("Please run main.py to start data processing")
