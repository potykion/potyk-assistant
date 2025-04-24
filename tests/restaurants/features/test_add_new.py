import pytest

from kys_in_rest.core.tg_utils import AskForData
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo


def test_add_new(rest_factory):
    add_new_rest = rest_factory.make_add_new_restaurant()
    repo: SqliteRestRepo = rest_factory.make_sqlite_rest_repo()

    with pytest.raises(AskForData):
        add_new_rest.do()

    rest, created = repo.get_or_create_draft()
    assert rest
    assert not created

    name = "test"
    for text in [
        name,
        "https://yandex.ru/maps/-/CHfaeW5p",
        "Китай Город",
    ]:
        try:
            add_new_rest.do(text)
        except AskForData:
            pass

    rest = repo.get_by_name(name)
    assert rest
    assert rest["yandex_maps"] == "https://yandex.ru/maps/-/CHfaeW5p"
    assert rest["metro"] == "Китай Город"
    assert bool(rest["draft"]) is False
