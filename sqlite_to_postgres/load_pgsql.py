import psycopg

from psycopg import ClientCursor
from psycopg.rows import dict_row
from dataclasses import dataclass, fields, astuple


def save_to_postgress(dsn: dict, table_name: str, rows_to_load: list[dataclass]):
    with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:
        # Очищаем таблицу в БД, чтобы загружать данные в пустую таблицу
        # cursor.execute("""CREATE TABLE IF NOT EXISTS content.temp_table (
        #                ID uuid PRIMARY KEY,
        #                full_name TEXT NOT NULL,
        #                  created timestamp with time zone,
        #                  updated timestamp with time zone)""")

        column_names = [field.name for field in fields(rows_to_load[0])]  # [id, name]
        column_names_str = ','.join(column_names)  # id, name
        col_count = ', '.join(['%s'] * len(column_names))  # '%s, %s
        bind_values = ','.join(cursor.mogrify(f"({col_count})", astuple(user)) for user in rows_to_load)
        query = (f'INSERT INTO content.{table_name} ({column_names_str}) VALUES {bind_values} '
                 f'ON CONFLICT (id) DO NOTHING')
        cursor.execute(query)


if __name__ == '__main__':
    print("Please run main.py to start data processing")
