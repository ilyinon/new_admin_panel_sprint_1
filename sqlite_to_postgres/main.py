import os

from uuid import UUID
from load.sqlite import load_from_sqlite
from load.pgsql import save_to_postgress
from load.dataclasses import User, Genre, FilmWork, GenreFilmWork, PersonFilmWork
from dotenv import load_dotenv

load_dotenv('/Users/oilyin/yandex/new_admin_panel_sprint_1/.env')

TABLES_TO_LOAD = ['person', 'genre', 'film_work', 'genre_film_work', 'person_film_work']


SQLITE_NUMBER_OF_ROWS_TO_FETCH = 100
PGSQL_ITER_SIZE = 100
DB_PATH = '/Users/oilyin/yandex/new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite'


dsn = {
    'dbname':os.environ.get('DB_NAME', 'movies_database'),
    'user': os.environ.get('DB_USER', 'app'),
    'password': os.environ.get('DB_PASSWORD',),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=content',
}


def map_sqlite_to_pgsql(table_name: str, el: dict):
    """
    Takes table_name to get colums format, el to get data from sqlite
    and converts table from sqlite schema to pgsql schema.
    """
    if table_name == 'person':
        return User(UUID(el['id']), el['full_name'], el['created_at'], 'NOW()')
    elif table_name == 'genre':
        return Genre(UUID(el['id']), el['name'], el['description'], el['created_at'], 'NOW()')
    elif table_name == 'film_work':
        return FilmWork(UUID(el['id']), el['title'], el['description'], el['creation_date'], '',
                        el['file_path'], el['rating'], el['type'], el['created_at'], el['updated_at'])
    elif table_name == 'genre_film_work':
        return GenreFilmWork(UUID(el['id']), UUID(el['film_work_id']), UUID(el['genre_id']), el['created_at'])
    elif table_name == 'person_film_work':
        return PersonFilmWork(UUID(el['id']), UUID(el['film_work_id']), UUID(el['person_id']), el['role'], el['created_at'])


def upload_data_from_sqlite_to_pgsql(table_name: str):
    """
    Takes table_name and calls load_from_sqlite() function to fetch_all data from sqlite.
    Each entry is formated to one of dataclasses to have a proper format.
    After it uploads data to postgres by using save_to_postgress()
    """

    loaded_data = []
    for el in load_from_sqlite(DB_PATH, table_name, SQLITE_NUMBER_OF_ROWS_TO_FETCH):
        loaded_data.append(map_sqlite_to_pgsql(table_name, el))
    save_to_postgress(dsn, table_name, loaded_data, PGSQL_ITER_SIZE)


if __name__ == '__main__':
    for table_to_load in TABLES_TO_LOAD:
        upload_data_from_sqlite_to_pgsql(table_to_load)
