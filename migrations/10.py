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
        INSERT INTO movies (title, image, kinopoisk_url, download_url, watch_url, why)
        VALUES ('Красивая работа',
                'https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/2b9b671e-4558-4d08-b114-4d6ac79f26dd/3840x',
                'https://www.kinopoisk.ru/film/119363/', 'https://rutracker.org/forum/viewtopic.php?t=3010430/', null,
                'сигма-муви по мнению <a href="https://t.me/rzhavuykholodez/95">ржавого холодца</a>');

        """
    )
    cursor.connection.commit()
