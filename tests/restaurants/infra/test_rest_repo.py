import sqlite3

import pytest

from kys_in_rest.core.str_utils import split_strip
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.infra.rest_repo import load_rests
from tests.cfg import tests_dir


@pytest.fixture
def cursor_test_db():
    conn = sqlite3.connect(tests_dir / "test_db.sqlite")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    return curr


@pytest.mark.parametrize("metro", metro_colors)
def test_load_rests(metro, cursor_test_db):
    rating = 7

    rests = load_rests(cursor_test_db, metro, rating)

    assert rests
    assert all(metro in split_strip(rest["metro"])   for rest in rests)
    assert all((rest["rating"] is None) or rest["rating"] >= rating for rest in rests)
