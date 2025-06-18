import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table if not exists wishlist
        (
            name     text,
            received TEXT
        );
        """
    )
    cursor.connection.commit()
