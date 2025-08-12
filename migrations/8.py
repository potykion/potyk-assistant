import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
     alter table my_tg_channels
    add description text;

     UPDATE my_tg_channels SET description = 'Личный рандом' WHERE name = 'Блядь, Лейбович!' AND link = 'https://t.me/+scHXi2m3_Q0zMTIy' AND icon = '🧑' AND description IS NULL AND rowid = 1;
     UPDATE my_tg_channels SET description = 'Мемцы' WHERE name = 'ржу приколы 25' AND link = 'https://t.me/rzhu_prikoly' AND icon = '😁' AND description IS NULL AND rowid = 2;
     UPDATE my_tg_channels SET description = 'Порнуха' WHERE name = 'порнушка джокера' AND link = 'https://t.me/+VcaHrRUEHuBjNTJi' AND icon = '🔞' AND description IS NULL AND rowid = 3;
     UPDATE my_tg_channels SET description = 'Прога, аи' WHERE name = 'Питон Пацан 2' AND link = 'https://t.me/potyk_python' AND icon = '🐍' AND description IS NULL AND rowid = 4;
     UPDATE my_tg_channels SET description = 'Рандом' WHERE name = 'Потик Спейс' AND link = 'https://t.me/potyk_space' AND icon = '👽' AND description IS NULL AND rowid = 5;
     UPDATE my_tg_channels SET description = 'Еда, рестики' WHERE name = 'надо по жра' AND link = 'https://t.me/po_zhra' AND icon = '🍔' AND description IS NULL AND rowid = 6;
     UPDATE my_tg_channels SET description = 'Тревел, места' WHERE name = 'потик тревел' AND link = 'https://t.me/potyk_travel' AND icon = '✈️' AND description IS NULL AND rowid = 7;
     UPDATE my_tg_channels SET description = 'Пиво, мед, сидр' WHERE name = 'пивомедсидр' AND link = 'https://t.me/beer_digest' AND icon = '🍺' AND description IS NULL AND rowid = 8;
     UPDATE my_tg_channels SET description = 'Клипы, треки, писанина про музык' WHERE name = 'potyk-mu' AND link = 'https://t.me/potyk_mu' AND icon = '🎵' AND description IS NULL AND rowid = 9;
            
        """
    )
    cursor.connection.commit()
