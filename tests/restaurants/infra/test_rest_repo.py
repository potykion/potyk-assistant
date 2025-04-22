import pytest

from kys_in_rest.core.str_utils import split_strip
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.prep.ioc import RestFactory
from tests.cfg import tests_dir


@pytest.mark.parametrize("metro", metro_colors)
def test_load_rests(metro):
    repo = RestFactory(tests_dir / "test_db.sqlite").make_sqlite_rest_repo()
    rating = 7

    rests = repo.list_restaurants(metro, rating)

    assert rests
    assert all(metro in split_strip(rest["metro"]) for rest in rests)
    assert all((rest["rating"] is None) or rest["rating"] >= rating for rest in rests)
