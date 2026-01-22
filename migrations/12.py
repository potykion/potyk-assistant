import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        create table mu_album
(
    id     integer not null
        constraint mu_album_pk
            primary key autoincrement,
    title  text    not null,
    artist text    not null,
    year   integer not null,
    cover  text    not null,
    link   text
);


        """
    )
    cursor.connection.commit()

