import datetime
from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.wishlist.entities.wishlist_item import WishlistItem
from kys_in_rest.wishlist.features.ports.wishlist_repo import WishlistRepo


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
        # Проверяем, есть ли уже такой предмет в полученных (поиск по началу названия)
        existing_received = self.cursor.execute(
            "SELECT * FROM wishlist WHERE name LIKE ? AND received IS NOT NULL",
            (f"{name}%",)
        ).fetchone()
        
        if existing_received:
            # Если предмет уже получен, сбрасываем флаг received
            item_name = existing_received['name']
            self.cursor.execute(
                "UPDATE wishlist SET received = NULL WHERE name = ?",
                (item_name,)
            )
            self.cursor.connection.commit()
            return WishlistItem(name=item_name)
        
        # Если предмета нет или он активный, добавляем новый
        item = WishlistItem(name=name)
        self.cursor.execute(
            f"INSERT INTO wishlist(name, received) VALUES (?, ?)",
            (item.name, item.received),
        )
        self.cursor.connection.commit()
        return item

    def mark_as_received(self, name: str) -> WishlistItem | None:
        # Ищем предмет по началу названия (LIKE)
        rows = self.cursor.execute(
            "SELECT * FROM wishlist WHERE name LIKE ? AND received IS NULL",
            (f"{name}%",)
        ).fetchall()
        
        if not rows:
            return None
        
        # Если найдено несколько предметов, берем первый
        row = rows[0]
        item_name = row['name']
        
        # Отмечаем как полученное
        received_date = datetime.datetime.now()
        self.cursor.execute(
            "UPDATE wishlist SET received = ? WHERE name = ? AND received IS NULL",
            (received_date, item_name)
        )
        self.cursor.connection.commit()
        
        return WishlistItem(name=item_name, received=received_date)
