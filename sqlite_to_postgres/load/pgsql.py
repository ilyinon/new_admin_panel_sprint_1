import psycopg

from psycopg import ClientCursor
from psycopg.rows import dict_row
from dataclasses import dataclass, fields, astuple


def save_to_postgress(dsn: dict, table_name: str, rows_to_load: list[dataclass], iter_size: str):
    """
    Takes prepared rows_to_load and insert it table_name with DSN.
    """
    with psycopg.connect(**dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn, conn.cursor() as cursor:

        cursor.itersize = iter_size
        column_names = [field.name for field in fields(rows_to_load[0])]  # [id, name]
        column_names_str = ','.join(column_names)  # id, name
        col_count = ', '.join(['%s'] * len(column_names))  # '%s, %s
        bind_values = ','.join(cursor.mogrify(f"({col_count})", astuple(user)) for user in rows_to_load)
        query = (f'INSERT INTO content.{table_name} ({column_names_str}) VALUES {bind_values} '
                 f'ON CONFLICT (id) DO NOTHING')
        cursor.execute(query)


if __name__ == '__main__':
    print("Please run main.py to start data processing")
