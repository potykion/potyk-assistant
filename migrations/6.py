import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """create table my_tg_channels
           (
               name text,
               link text,
               constraint my_tg_channels_pk
                   unique (name, link)
           );

        INSERT INTO my_tg_channels (name, link)
        VALUES ('Блядь, Лейбович!', 'https://t.me/+scHXi2m3_Q0zMTIy');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('ржу приколы 25', 'https://t.me/rzhu_prikoly');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('порнушка джокера', 'https://t.me/+VcaHrRUEHuBjNTJi');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('Питон Пацан 2', 'https://t.me/potyk_python');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('Потик Спейс', 'https://t.me/potyk_space');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('надо по жра', 'https://t.me/po_zhra');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('потик тревел', 'https://t.me/potyk_travel');
        INSERT INTO my_tg_channels (name, link)
        VALUES ('пивомедсидр', 'https://t.me/beer_digest');

        """
    )
    cursor.connection.commit()
