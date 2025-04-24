from functools import cached_property

from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.restaurants.features.add_new import AddNewRestaurant
from kys_in_rest.restaurants.features.near import GetNearRestaurants
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo


class RestFactory:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @cached_property
    def sqlite_cursor(self):
        return make_sqlite_cursor(self.db_path)

    def make_get_near_restaurants(self):
        return GetNearRestaurants(self.make_sqlite_rest_repo())

    def make_add_new_restaurant(self):
        return AddNewRestaurant(self.make_sqlite_rest_repo())

    def make_sqlite_rest_repo(self):
        return SqliteRestRepo(self.sqlite_cursor)

    def make_slite_flow_repo(self):
        return SqliteFlowRepo(self.sqlite_cursor)
