import sqlite3

from kys_in_rest.beer.features.add_new_beer import AddNewBeer
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.infra.beer_post_repo import SqliteBeerPostRepo
from kys_in_rest.core.ioc import IOC
from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.health.features.add_weight import AddOrShowWeight
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.health.infra.weight_repo import SqliteWeightRepo
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.find_near_category import (
    GetNearRestaurants,
    FindCategoryRestaurants,
)
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.features.id import ShowTgId
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin


def make_ioc(
    *,
    db_path: str,
    tg_admins: list[int],
) -> IOC:
    ioc = IOC()

    # deps
    ioc.register("db_path", db_path)
    ioc.register("tg_admins", tg_admins)
    ioc.register(
        sqlite3.Cursor,
        make_sqlite_cursor,
        cache=True,
        teardown=lambda cursor: cursor.connection.close(),
    )

    # repos
    ioc.register(RestRepo, SqliteRestRepo)
    ioc.register(FlowRepo, SqliteFlowRepo)
    ioc.register(BeerPostRepo, SqliteBeerPostRepo)
    ioc.register(WeightRepo, SqliteWeightRepo)

    # use-cases
    ioc.register(CheckTgAdmin, CheckTgAdmin)
    ioc.register(GetNearRestaurants, GetNearRestaurants)
    ioc.register(AddNewRestaurant, AddNewRestaurant)
    ioc.register(AddNewBeer, AddNewBeer)
    ioc.register(FindCategoryRestaurants, FindCategoryRestaurants)
    ioc.register(AddOrShowWeight, AddOrShowWeight)
    ioc.register(ShowTgId, ShowTgId)

    return ioc
