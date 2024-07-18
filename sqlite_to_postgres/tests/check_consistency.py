import psycopg
import unittest
from psycopg import ClientCursor
from psycopg.rows import dict_row
from dataclasses import dataclass, fields, astuple
import sqlite3
from contextlib import contextmanager
from collections import defaultdict


TABLES_TO_LOAD = ['person', 'genre', 'film_work', 'genre_film_work', 'person_film_work']
DB_PATH = '/Users/oilyin/yandex/new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite'
PG_SCHEMA_NAME = 'content'
TABLES_TO_CHECK = [
    {'table_name': 'person',
        'psql_query': 'SELECT id::text, full_name FROM content.person ORDER BY id;',
        'sqlite_query': 'SELECT id, full_name FROM person ORDER BY id;'
     },
    {'table_name': 'genre',
        'psql_query': 'SELECT id::text, name, description FROM content.genre ORDER BY id;',
        'sqlite_query': 'SELECT id, name, description FROM genre ORDER BY id;'
     },
    {'table_name': 'film_work',
        'psql_query': 'SELECT id::text, title, description, file_path, rating, type, creation_date FROM content.film_work ORDER BY id;',
        'sqlite_query': 'SELECT id, title, description, file_path, rating, type, creation_date FROM film_work ORDER BY id;'
     },
    {'table_name': 'genre_film_work',
        'psql_query': 'SELECT id::text, film_work_id::text, genre_id::text FROM content.genre_film_work ORDER BY id;',
        'sqlite_query': 'SELECT id, film_work_id, genre_id FROM genre_film_work ORDER BY id;'
     },
    {'table_name': 'person_film_work',
        'psql_query': 'SELECT id::text, film_work_id::text, person_id::text, role FROM content.person_film_work ORDER BY id;',
        'sqlite_query': 'SELECT id, film_work_id, person_id, role FROM person_film_work ORDER BY id;'
     },
]
dsn = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}


@contextmanager
def conn_context(db_path: str):
    """
    Takes sqlite db_path to prepare connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def dict_factory(cursor, row):
    d = {}  # Создаем пустой словарь
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]  # Заполняем его значениями
    return d


class TestDatabaseConsistency(unittest.TestCase):

    def test_tables_existence(self):
        """
        Takes tables from table_schema and verify if all tables from list TABLES_TO_LOAD are exist
        """
        current_pg_tables = []
        with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
            query = (f'SELECT table_name FROM information_schema.tables WHERE table_schema = \'{PG_SCHEMA_NAME}\';')
            cursor.execute(query)
            for entry in cursor.fetchall():
                current_pg_tables.append(entry['table_name'])
            for table in TABLES_TO_LOAD:
                self.assertIn(table, current_pg_tables, f"Table {table} isn't present in PGSQL.")

    def test_verify_number_enties_in_table_is_equal(self):
        """
        Executes count query for each of tables from TABLES_TO_LOAD and compare if their amount is equal
        """
        for table in TABLES_TO_LOAD:
            with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
                query = (f'SELECT COUNT(*) FROM content.{table};')
                cursor.execute(query)
                pgsql_count = cursor.fetchall()[0]['count']

            with conn_context(DB_PATH) as conn:
                curs = conn.cursor()
                curs.execute(f"SELECT count(*) FROM {table};")
                sqlite_count = dict(curs.fetchmany()[0])['count(*)']
            self.assertEqual(pgsql_count, sqlite_count, f"Amount of entries are not equal in  {table} table.")

    def test_all_entries_in_tables_are_equal(self):
        """
        Takes entries from tables by TABLES_TO_CHECK list of dictionaries. Each dictionary containes
        name of tables and specified query for sqlite and pgsql.
        After all data are fetched and put to dictionaries, it compares these dicts.
        If you have a lot of entries in any table this check will work extremally slow.
        """
        for table in TABLES_TO_CHECK:
            with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
                query = (table['psql_query'])
                cursor.execute(query)
                pg_all = cursor.fetchall()

            with conn_context(DB_PATH) as conn:
                conn.row_factory = dict_factory
                curs = conn.cursor()
                curs.execute(table['sqlite_query'])
                # curs.execute(f"SELECT id, full_name FROM {table};")
                sqlite_all = curs.fetchall()
            self.assertEqual(pg_all, sqlite_all, f"Entries are not equal in {table}")


if __name__ == '__main__':
    for table in TABLES_TO_LOAD:
        unittest.main()
