import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
    create table if not exists weight
    (
        date   TEXT,
        weight REAL
    );
    """
    )
    cursor.executescript(
        """
    INSERT INTO weight (date, weight) VALUES ('2025-05-22', 82.6);
    INSERT INTO weight (date, weight) VALUES ('2025-05-30', 81.8);
    INSERT INTO weight (date, weight) VALUES ('2024-08-27', 81.5);
    INSERT INTO weight (date, weight) VALUES ('2024-09-17', 80.1);
    INSERT INTO weight (date, weight) VALUES ('2024-10-01', 78.6);
    INSERT INTO weight (date, weight) VALUES ('2024-10-03', 79.1);
    INSERT INTO weight (date, weight) VALUES ('2024-10-09', 79);
    INSERT INTO weight (date, weight) VALUES ('2024-10-15', 78);
    INSERT INTO weight (date, weight) VALUES ('2024-10-19', 78.2);
    INSERT INTO weight (date, weight) VALUES ('2024-10-29', 78.6);
    INSERT INTO weight (date, weight) VALUES ('2024-10-31', 78.4);
    INSERT INTO weight (date, weight) VALUES ('2024-11-05', 77.9);
    INSERT INTO weight (date, weight) VALUES ('2024-11-16', 80.6);
    INSERT INTO weight (date, weight) VALUES ('2024-11-21', 80.1);
    INSERT INTO weight (date, weight) VALUES ('2024-11-28', 79.5);
    INSERT INTO weight (date, weight) VALUES ('2024-12-03', 78.9);
    INSERT INTO weight (date, weight) VALUES ('2024-12-05', 79.8);
    INSERT INTO weight (date, weight) VALUES ('2024-12-10', 80);
    INSERT INTO weight (date, weight) VALUES ('2024-12-12', 80.4);
    INSERT INTO weight (date, weight) VALUES ('2024-12-17', 79.9);
    INSERT INTO weight (date, weight) VALUES ('2024-12-19', 79.9);
    INSERT INTO weight (date, weight) VALUES ('2025-01-09', 80.3);
    INSERT INTO weight (date, weight) VALUES ('2025-01-13', 81);
    INSERT INTO weight (date, weight) VALUES ('2025-01-16', 81.3);
    INSERT INTO weight (date, weight) VALUES ('2025-01-20', 80.6);
    INSERT INTO weight (date, weight) VALUES ('2025-01-27', 80.4);
    INSERT INTO weight (date, weight) VALUES ('2025-01-31', 82);
    INSERT INTO weight (date, weight) VALUES ('2025-02-03', 80.8);
    INSERT INTO weight (date, weight) VALUES ('2025-02-11', 81.2);
    INSERT INTO weight (date, weight) VALUES ('2025-02-13', 82.5);
    INSERT INTO weight (date, weight) VALUES ('2025-02-17', 81);
    INSERT INTO weight (date, weight) VALUES ('2025-02-18', 83);
    INSERT INTO weight (date, weight) VALUES ('2025-02-24', 81.3);
    INSERT INTO weight (date, weight) VALUES ('2025-02-27', 81.8);
    INSERT INTO weight (date, weight) VALUES ('2025-03-04', 81.4);
    INSERT INTO weight (date, weight) VALUES ('2025-03-15', 80.3);
    INSERT INTO weight (date, weight) VALUES ('2025-03-20', 81.7);
    INSERT INTO weight (date, weight) VALUES ('2025-03-27', 82.2);
    INSERT INTO weight (date, weight) VALUES ('2025-03-31', 82);
    INSERT INTO weight (date, weight) VALUES ('2025-04-11', 82.8);
    INSERT INTO weight (date, weight) VALUES ('2025-04-21', 83.2);
    INSERT INTO weight (date, weight) VALUES ('2025-05-07', 82.4);
    INSERT INTO weight (date, weight) VALUES ('2025-05-13', 80);
    INSERT INTO weight (date, weight) VALUES ('2025-05-15', 82.7);
    """
    )
    cursor.connection.commit()
