import sqlite3

from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.features.ports import RestRepo


def load_rests(cursor: sqlite3.Cursor, metro=None, rating=None) -> list[Restaurant]:
    q = "select * from restaurants"
    params = []

    where_parts = []

    if metro:
        where_parts.append("(metro like ?)")
        params.append(f"%{metro}%")
    if rating:
        where_parts.append("(rating is null or rating >= ?)")
        params.append(rating)

    if where_parts:
        q = f"{q} where {' AND '.join(where_parts)}"

    rows = cursor.execute(q, params).fetchall()
    return [Restaurant(**row) for row in rows]


class SqliteRestRepo(RestRepo):
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def get_or_create_draft(self) -> Restaurant:
        pass

    ...

