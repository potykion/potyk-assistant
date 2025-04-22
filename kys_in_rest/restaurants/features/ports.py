import abc

from kys_in_rest.restaurants.entries.restaurant import Restaurant


class RestRepo:
    @abc.abstractmethod
    def get_or_create_draft(self) -> Restaurant:
        ...


    @abc.abstractmethod
    def list_restaurants(self, metro=None, rating=None) -> list[Restaurant]:
        ...
