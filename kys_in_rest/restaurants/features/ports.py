import abc

from kys_in_rest.restaurants.entries.restaurant import Restaurant


class RestRepo:
    @abc.abstractmethod
    def get_or_create_draft(self) -> tuple[Restaurant, bool]: ...

    @abc.abstractmethod
    def list_restaurants(
        self,
        *,
        tags: list[str] = None,
        metro: str = None,
        rating: int = None,
    ) -> list[Restaurant]: ...

    @abc.abstractmethod
    def update_draft(self, rest: Restaurant) -> None: ...

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Restaurant: ...

    @abc.abstractmethod
    def delete_by_name(self, name: str) -> None: ...

    @abc.abstractmethod
    def check_name_unique(self, name: str) -> bool: ...
