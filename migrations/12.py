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
INSERT INTO mu_album (title, artist, year, cover, link) VALUES ('Driving Insane', 'Black Sun Empire', 2004, 'https://avatars.yandex.net/get-music-content/119639/3fff4e3d.a.5852040-1/600x600', 'https://music.yandex.ru/album/5852040');


        """
    )
    cursor.connection.commit()

