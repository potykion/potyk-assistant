import abc

from kys_in_rest.restaurants.entries.restaurant import Restaurant


class RestRepo:
    @abc.abstractmethod
    def get_or_create_draft(self) -> Restaurant: ...

    @abc.abstractmethod
    def list_restaurants(
        self,
        *,
        tags=None,
        metro=None,
        rating=None,
    ) -> list[Restaurant]: ...

    @abc.abstractmethod
    def update_draft(self, rest): ...

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Restaurant: ...

    @abc.abstractmethod
    def delete_by_name(self, name: str): ...

    @abc.abstractmethod
    def check_name_unique(self, name: str) -> bool: ...
