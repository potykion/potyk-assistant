import sqlite3

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.restaurants.entries.restaurant import Restaurant


def load_rests(metro=None, rating=None):
    conn = sqlite3.connect(root_dir / "db.sqlite")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()

    q = "select * from restaurants"
    params = []

    where = []

    if metro:
        q = f"metro like ?"
        params.append(f"%{metro}%")
    if rating:
        q = f"rating is null or rating >= ?"
        params.append("?")

    if where:
        q = f"{q} where {' AND '.join(where)}"

    rows = curr.execute(q, params).fetchall()
    return [Restaurant(**row) for row in rows]
