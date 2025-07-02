import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table spendings
        (
            created_dt TEXT not null,
            amount     real not null,
            comment    TEXT not null
        );
        """
    )
    cursor.connection.commit()
