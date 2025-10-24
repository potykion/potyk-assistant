import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table untappd_checkins
(
    id                   integer
        constraint untappd_checkins_pk
            primary key,
    beer_url             text,
    beer_img             text,
    beer_name            text,
    beer_brewery         text,
    beer_brewery_url     text,
    checkin_location     text,
    checkin_location_url text,
    checkin_comment      TEXT,
    checkin_rating       REAL,
    checkin_date         text
);


        """
    )
    cursor.connection.commit()


