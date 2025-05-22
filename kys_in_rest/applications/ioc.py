import sqlite3
from functools import cached_property

from kys_in_rest.beer.features.add_new_beer import AddNewBeer
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.infra.beer_post_repo import SqliteBeerPostRepo
from kys_in_rest.core.ioc import IOC
from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.find_near_category import (
    GetNearRestaurants,
    FindCategoryRestaurants,
)
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo


def make_ioc(db_path: str) -> IOC:
    ioc = IOC()

    ioc.register("db_path", db_path)
    ioc.register(
        sqlite3.Cursor,
        make_sqlite_cursor,
        cache=True,
        teardown=lambda cursor: cursor.connection.close(),
    )

    ioc.register(RestRepo, SqliteRestRepo)
    ioc.register(FlowRepo, SqliteFlowRepo)
    ioc.register(BeerPostRepo, SqliteBeerPostRepo)

    ioc.register(GetNearRestaurants, GetNearRestaurants)
    ioc.register(AddNewRestaurant, AddNewRestaurant)
    ioc.register(AddNewBeer, AddNewBeer)
    ioc.register(FindCategoryRestaurants, FindCategoryRestaurants)

    return ioc


class MainFactory:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @cached_property
    def sqlite_cursor(self):
        return make_sqlite_cursor(self.db_path)

    def teardown(self):
        self.sqlite_cursor.connection.close()

    def make_rest_repo(self) -> RestRepo:
        return SqliteRestRepo(self.sqlite_cursor)

    def make_flow_repo(self) -> FlowRepo:
        return SqliteFlowRepo(self.sqlite_cursor)

    def make_beer_post_repo(self) -> BeerPostRepo:
        return SqliteBeerPostRepo(self.sqlite_cursor)

    def make_get_near_restaurants(self):
        return GetNearRestaurants(self.make_rest_repo())

    def make_add_new_restaurant(self):
        return AddNewRestaurant(self.make_rest_repo())

    def make_add_new_beer(self):
        return AddNewBeer(self.make_beer_post_repo())

    def make_find_category_restaurants(self):
        return FindCategoryRestaurants(self.make_rest_repo())
