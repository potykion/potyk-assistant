import sqlite3

import pytest

from kys_in_rest.core.cfg import root_dir
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.infra.rest_repo import load_rests
from tests.cfg import tests_dir


@pytest.fixture
def cursor_test_db():
    conn = sqlite3.connect(tests_dir / "test_db.sqlite")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    return curr


@pytest.mark.parametrize("metro", ["Новослободская", "Лубянка"])
def test_load_rests(metro, cursor_test_db):
    rating = 7
    rests = load_rests(cursor_test_db, metro, rating)

    assert rests
    assert all(rest["metro"] == metro for rest in rests)
    assert all(rest["rating"] is None or rest["rating"] >= rating for rest in rests)
