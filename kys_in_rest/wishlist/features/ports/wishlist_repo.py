import abc

from kys_in_rest.wishlist.entities.wishlist_item import WishlistItem


class WishlistRepo(abc.ABC):
    @abc.abstractmethod
    def list_not_received(self) -> list[WishlistItem]: ...

    @abc.abstractmethod
    def list_received(self) -> list[WishlistItem]: ...

    @abc.abstractmethod
    def add(self, name: str) -> WishlistItem: ...

    @abc.abstractmethod
    def mark_as_received(self, name: str) -> WishlistItem | None: ...

    @abc.abstractmethod
    def delete(self, name: str) -> WishlistItem | None: ...
