import pytest

from kys_in_rest.core.str_utils import split_strip
from kys_in_rest.restaurants.entries.metro import metro_colors


def test_list_restaurants(rest_repo):
    metro = "Алексеевская"
    rating = 7

    rest, _ = rest_repo.get_or_create_draft()
    rest.update({
        "name": "test",
        "yandex_maps": "test",
        "metro": metro,
        "tags": "Вьетнамка🥋",
        "rating": rating,
    })
    rest_repo.update_draft(rest)

    rests = rest_repo.list_restaurants(metro=metro, rating=rating)

    assert rests
    assert all(metro in split_strip(rest["metro"]) for rest in rests)
    assert all((rest["rating"] is None) or rest["rating"] >= rating for rest in rests)


def test_get_or_create_draft(rest_repo):
    rest, created = rest_repo.get_or_create_draft()
    assert rest
    assert rest["draft"]
    assert created

    rest, created = rest_repo.get_or_create_draft()
    assert rest
    assert not created
    assert rest["draft"]
    drafts = rest_repo.cursor.execute(
        "select * from restaurants where draft = 1"
    ).fetchall()
    assert len(drafts) == 1

    rest_repo.cursor.execute("update restaurants set name = 'test' where draft = 1")
    rest_repo.cursor.connection.commit()
    rest, _ = rest_repo.get_or_create_draft()

    assert rest["name"] == "test"


def test_update_draft(rest_repo):
    rest, _ = rest_repo.get_or_create_draft()

    rest["name"] = "test2"
    rest_repo.update_draft(rest)

    rest, _ = rest_repo.get_or_create_draft()
    assert rest["name"] == "test2"
