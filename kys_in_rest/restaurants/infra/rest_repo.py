import sqlite3

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.restaurants.entries.restaurant import Restaurant


def load_rests(metro=None):
    conn = sqlite3.connect(root_dir / "db.sqlite")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()

    q = "select * from restaurants"
    params = tuple()
    if metro:
        q = "select * from restaurants where metro like ?"
        params = (f"%{metro}%",)

    rows = curr.execute(q, params).fetchall()
    return [Restaurant(**row) for row in rows]
