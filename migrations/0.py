import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table if not exists "beer_posts"
        (
            created TEXT,
            beers   text,
            id      integer not null
                constraint beer_posts_pk
                    primary key autoincrement
        );
        
        create table if not exists flow
        (
            command TEXT
            , tg_user_id integer);
        
        create table if not exists "restaurants"
        (
            name         TEXT,
            yandex_maps  TEXT,
            tags         TEXT,
            city         TEXT,
            metro        TEXT,
            prices       TEXT,
            rating       INTEGER,
            comment      TEXT,
            date_created TEXT,
            telegram     TEXT,
            site         TEXT,
            owner        TEXT,
            chief        TEXT,
            visited      integer,
            from_channel TEXT,
            from_post    TEXT
            , draft integer);
        """
    )
    cursor.connection.commit()
