import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        CREATE TABLE "beer_posts"
        (
            created TEXT,
            beers   text,
            id      integer not null
                constraint beer_posts_pk
                    primary key autoincrement
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE flow
        (
            command TEXT
            , tg_user_id integer);
        """
    )
    cursor.execute(
        """
        CREATE TABLE "restaurants"
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
