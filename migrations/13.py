import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table tags
        (
            id       integer not null
                constraint tags_pk
                    primary key autoincrement,
            title    text    not null,
            entity_type text    not null
        );
        create table tag_m2m
        (
            tag_id      integer not null,
            entity_id   integer not null,
            entity_type text    not null
        );
INSERT INTO tags (title, entity_type) VALUES ('dnb', 'mu_album');
INSERT INTO tags (title, entity_type) VALUES ('trip-hop', 'mu_album');

        """
    )
    cursor.connection.commit()


