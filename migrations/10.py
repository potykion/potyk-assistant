import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table movies
        (
            id            integer not null
                constraint movies_pk
                    primary key autoincrement,
            title         TEXT,
            image         text,
            kinopoisk_url TEXT,
            download_url  TEXT,
            watch_url     TEXT,
            why           TEXT
        );


        """
    )
    cursor.connection.commit()
