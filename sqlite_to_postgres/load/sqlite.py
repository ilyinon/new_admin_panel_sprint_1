import sqlite3
from contextlib import contextmanager


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


def load_from_sqlite(db_path: str, table_name_to_load: str, rows_to_fetch: str):
    """
    Takes db_path to load data from provided table_name by chunk size rows_to_fetch
    """
    try:
        with conn_context(db_path) as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT * FROM {table_name_to_load};")
            results = []
            while True:
                data = curs.fetchmany(size=rows_to_fetch)
                if not data:
                    return results
                for item in data:
                    results.append(dict(item))
    except sqlite3.Error as ex:
        print(f"SQLITE: Error during reading from {table_name_to_load}", ex)


if __name__ == '__main__':
    print("Please run main.py to start data processing")
