from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.wishlist.entities.wishlist_item import WishlistItem
from kys_in_rest.wishlist.features.wishlist import WishlistRepo


class SqliteWishlistRepo(SqliteRepo, WishlistRepo):
    def list_not_received(self) -> list[WishlistItem]:
        rows = self.cursor.execute(
            "SELECT * FROM wishlist where received is null"
        ).fetchall()
        return [WishlistItem(**row) for row in rows]

    def add(self, name: str) -> WishlistItem:
        item = WishlistItem(name=name)
        self.cursor.execute(
            f"INSERT INTO wishlist(name, received) VALUES (?, ?)",
            (item.name, item.received),
        )
        self.cursor.connection.commit()
        return item
