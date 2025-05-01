from functools import cached_property

from kys_in_rest.beer.add_new_beer import AddNewBeer
from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.near import GetNearRestaurants
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo


class RestFactory:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @cached_property
    def sqlite_cursor(self):
        return make_sqlite_cursor(self.db_path)

    def make_get_near_restaurants(self):
        return GetNearRestaurants(self.make_rest_repo())

    def make_add_new_restaurant(self):
        return AddNewRestaurant(self.make_rest_repo())

    def make_add_new_beer(self):
        return AddNewBeer()

    def make_rest_repo(self) -> RestRepo:
        return SqliteRestRepo(self.sqlite_cursor)

    def make_flow_repo(self) -> FlowRepo:
        return SqliteFlowRepo(self.sqlite_cursor)
