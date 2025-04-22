import sqlite3

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.restaurants.entries.restaurant import Restaurant


def load_rests(metro=None, rating=None):
    conn = sqlite3.connect(root_dir / "db.sqlite")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()

    q = "select * from restaurants"
    params = []

    where_parts = []

    if metro:
        where_parts.append("metro like ?")
        params.append(f"%{metro}%")
    if rating:
        where_parts.append("rating is null or rating >= ?")
        params.append("?")

    if where_parts:
        q = f"{q} where {' AND '.join(where_parts)}"

    rows = curr.execute(q, params).fetchall()
    return [Restaurant(**row) for row in rows]
