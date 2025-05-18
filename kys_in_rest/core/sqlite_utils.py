import sqlite3


def make_sqlite_cursor(db_path: str) -> sqlite3.Cursor:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


class SqliteRepo:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
