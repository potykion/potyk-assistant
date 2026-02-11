import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        ALTER TABLE movies ADD COLUMN dropped INTEGER DEFAULT 0;
        """
    )
    cursor.connection.commit()
