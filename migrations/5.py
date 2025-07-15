import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table config
        (
            config_json text,
            id          integer not null
                constraint config_pk
                    primary key autoincrement
        );
        create table zen_money_diff
        (
            server_timestamp integer,
            diff             text
        );


        """
    )
    cursor.connection.commit()
