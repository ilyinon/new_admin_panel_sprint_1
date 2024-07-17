from uuid import UUID

from load.sqlite import load_from_sqlite
from load.pgsql import save_to_postgress
from load.dataclasses import User, Genre, FilmWork, GenreFilmWork, PersonFilmWork


SQLITE_NUMBER_OF_ROWS_TO_FETCH = 100
DB_PATH = '/Users/oilyin/yandex/new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite'
TABLES_TO_LOAD = ['person', 'genre', 'film_work', 'genre_film_work', 'person_film_work']

dsn = {
    'dbname': 'mdb',
    'user': 'app',
    'password': '123qwe',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}


def upload_data_from_sqlite_to_pgsql(table_name: str):
    """
    Takes table_name and calls load_from_sqlite() function which fetch all data from sqlite.
    Each entry is formated to one of dataclasses to have a proper format.
    After it uploads data to postgres by using save_to_postgress()
    """

    loaded_data = []
    for el in load_from_sqlite(DB_PATH, table_name, SQLITE_NUMBER_OF_ROWS_TO_FETCH):
        if table_name == 'person':
            to_append = User(UUID(el['id']), el['full_name'], el['created_at'], 'NOW()')
        elif table_name == 'genre':
            to_append = Genre(UUID(el['id']), el['name'], el['description'], el['created_at'], 'NOW()')
        elif table_name == 'film_work':
            to_append = FilmWork(UUID(el['id']), el['title'], el['description'], el['creation_date'], '', el['file_path'],
                                 el['rating'], el['type'], el['created_at'], el['updated_at'])
        elif table_name == 'genre_film_work':
            to_append = GenreFilmWork(UUID(el['id']), UUID(el['film_work_id']), UUID(el['genre_id']), el['created_at'])
        elif table_name == 'person_film_work':
            to_append = PersonFilmWork(UUID(el['id']), UUID(el['film_work_id']), UUID(el['person_id']), el['role'], el['created_at'])
        loaded_data.append(to_append)
    save_to_postgress(dsn, table_name, loaded_data)


if __name__ == '__main__':
    for table_to_load in TABLES_TO_LOAD:
        upload_data_from_sqlite_to_pgsql(table_to_load)
