import os

import pytest

from kys_in_rest.core.tg_utils import AskForData
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


def test_add_new(ioc, tg_admin_user_id):
    add_new_rest = ioc.resolve(AddNewRestaurant)
    repo: SqliteRestRepo = ioc.resolve(RestRepo)

    with pytest.raises(AskForData):
        add_new_rest.do(InputTgMsg(text=None, tg_user_id=tg_admin_user_id))

    rest, created = repo.get_or_create_draft()
    assert rest
    assert not created

    name = "test"
    for text in [
        name,
        "https://yandex.ru/maps/-/CHfaeW5p",
        "Китай Город",
        "Сербия 🫓",
        "-",
        "comment",
    ]:
        try:
            add_new_rest.do(InputTgMsg(text=text, tg_user_id=tg_admin_user_id))
        except AskForData:
            pass

    rest = repo.get_by_name(name)
    assert rest
    assert rest["yandex_maps"] == "https://yandex.ru/maps/-/CHfaeW5p"
    assert rest["metro"] == "Китай Город"
    assert bool(rest["draft"]) is False

    with pytest.raises(AskForData) as e:
        add_new_rest.do(InputTgMsg(text=name, tg_user_id=tg_admin_user_id))
        assert e.value.messages[0].message == "Такой рестик уже был, введи другой"
