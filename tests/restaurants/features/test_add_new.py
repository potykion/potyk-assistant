import pytest

from kys_in_rest.core.tg_utils import AskForData


def test_add_new(rest_factory):
    add_new_rest = rest_factory.make_add_new_restaurant()
    repo = rest_factory.make_sqlite_rest_repo()

    with pytest.raises(AskForData):
        add_new_rest.do()

    rest, created = repo.get_or_create_draft()
    assert rest
    assert not created

    for text in [
        "test",
        "https://yandex.ru/maps/-/CHfaeW5p",
        "Китай Город",
    ]:
        try:
            rest = add_new_rest.do(text)
        except AskForData:
            pass

    assert rest["name"] == "test"
    assert rest["yandex_maps"] == "https://yandex.ru/maps/-/CHfaeW5p"
    assert rest["metro"] == "Китай Город"
    assert rest["draft"] is False
