import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        
        INSERT INTO my_tg_channels (name, link) VALUES ('potyk-mu', 'https://t.me/potyk_mu');
            
        alter table my_tg_channels add icon text;
            
        UPDATE my_tg_channels SET icon = '🐍' WHERE name = 'Питон Пацан 2' AND link = 'https://t.me/potyk_python' AND icon IS NULL AND rowid = 4;
        UPDATE my_tg_channels SET icon = '🎵' WHERE name = 'potyk-mu' AND link = 'https://t.me/potyk_mu' AND icon IS NULL AND rowid = 9;
        UPDATE my_tg_channels SET icon = '🔞' WHERE name = 'порнушка джокера' AND link = 'https://t.me/+VcaHrRUEHuBjNTJi' AND icon IS NULL AND rowid = 3;
        UPDATE my_tg_channels SET icon = '👽' WHERE name = 'Потик Спейс' AND link = 'https://t.me/potyk_space' AND icon IS NULL AND rowid = 5;
        UPDATE my_tg_channels SET icon = '✈️' WHERE name = 'потик тревел' AND link = 'https://t.me/potyk_travel' AND icon IS NULL AND rowid = 7;
        UPDATE my_tg_channels SET icon = '🍔' WHERE name = 'надо по жра' AND link = 'https://t.me/po_zhra' AND icon IS NULL AND rowid = 6;
        UPDATE my_tg_channels SET icon = '🍺' WHERE name = 'пивомедсидр' AND link = 'https://t.me/beer_digest' AND icon IS NULL AND rowid = 8;
        UPDATE my_tg_channels SET icon = '🧑' WHERE name = 'Блядь, Лейбович!' AND link = 'https://t.me/+scHXi2m3_Q0zMTIy' AND icon IS NULL AND rowid = 1;
        UPDATE my_tg_channels SET icon = '😁' WHERE name = 'ржу приколы 25' AND link = 'https://t.me/rzhu_prikoly' AND icon IS NULL AND rowid = 2;
            
            
        """
    )
    cursor.connection.commit()
