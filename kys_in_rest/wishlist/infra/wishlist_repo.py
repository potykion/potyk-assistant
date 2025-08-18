import datetime
from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.wishlist.entities.wishlist_item import WishlistItem
from kys_in_rest.wishlist.features.wishlist import WishlistRepo


class SqliteWishlistRepo(SqliteRepo, WishlistRepo):
    def list_not_received(self) -> list[WishlistItem]:
        rows = self.cursor.execute(
            "SELECT * FROM wishlist where received is null"
        ).fetchall()
        return [WishlistItem(**row) for row in rows]

    def list_received(self) -> list[WishlistItem]:
        rows = self.cursor.execute(
            "SELECT * FROM wishlist where received is not null ORDER BY received DESC"
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

    def mark_as_received(self, name: str) -> WishlistItem | None:
        # Сначала найдем предмет
        row = self.cursor.execute(
            "SELECT * FROM wishlist WHERE name = ? AND received IS NULL",
            (name,)
        ).fetchone()
        
        if not row:
            return None
        
        # Отмечаем как полученное
        received_date = datetime.datetime.now()
        self.cursor.execute(
            "UPDATE wishlist SET received = ? WHERE name = ? AND received IS NULL",
            (received_date, name)
        )
        self.cursor.connection.commit()
        
        return WishlistItem(name=name, received=received_date)
