import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table mon_goals
        (
            due_date TEXT,
            val      real,
            category text
        );
        """
    )
    cursor.connection.commit()
