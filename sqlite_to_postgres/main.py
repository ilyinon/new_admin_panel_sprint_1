from dataclasses import dataclass, fields, asdict, astuple
from uuid import UUID
import datetime

from load_sqlite import load_from_sqlite
from load_pgsql import save_to_postgress


SQLITE_NUMBER_OF_ROWS_TO_FETCH = 100
DB_PATH = '/Users/oilyin/yandex/new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite'

dsn = {
    'dbname': 'mdb',
    'user': 'app',
    'password': '123qwe',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}


@dataclass
class User:
    id: UUID
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime


loaded_data = []


def upload_data_from_sqlite_to_pgsql(dbname: str):
    for el in load_from_sqlite(DB_PATH, 'person', SQLITE_NUMBER_OF_ROWS_TO_FETCH):
        if dbname == 'person':
            to_append = User(UUID(el['id']), el['full_name'], el['created_at'], 'NOW()')
        loaded_data.append(to_append)
    save_to_postgress(dsn, dbname, loaded_data)


if __name__ == '__main__':

    upload_data_from_sqlite_to_pgsql('person')
