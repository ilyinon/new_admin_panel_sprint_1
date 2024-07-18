import psycopg
import unittest
from psycopg import ClientCursor
from psycopg.rows import dict_row
from dataclasses import dataclass, fields, astuple
import sqlite3
from contextlib import contextmanager

TABLES_TO_LOAD = ['person', 'genre', 'film_work', 'genre_film_work', 'person_film_work']
DB_PATH = '/Users/oilyin/yandex/new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite'
PG_SCHEMA_NAME = 'content'
dsn = {
    'dbname': 'mdb',
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


class TestDatabaseConsistency(unittest.TestCase):

    def test_tables_existence(self):
        current_pg_tables = []
        with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
            query = (f'SELECT table_name FROM information_schema.tables WHERE table_schema = \'{PG_SCHEMA_NAME}\';')
            cursor.execute(query)
            for entry in cursor.fetchall():
                current_pg_tables.append(entry['table_name'])
            for table in TABLES_TO_LOAD:
                self.assertIn(table, current_pg_tables, f"Table {table} isn't present in PGSQL.")

    def test_verify_number_enties_in_table_is_equal(self):
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


if __name__ == '__main__':
    for table in TABLES_TO_LOAD:
        # test_verify_number_enties_in_table_is_equal(dsn, table)
        # test_tables_eixtence(dsn, table)
        unittest.main()
