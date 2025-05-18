import sqlite3

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.features.ports import RestRepo


class SqliteRestRepo(RestRepo, SqliteRepo):

    def get_or_create_draft(self) -> tuple[Restaurant, bool]:
        row = self.cursor.execute(
            "select * from restaurants where draft = 1"
        ).fetchone()
        if not row:
            self.cursor.execute("""insert into restaurants (draft) values (1);""")
            self.cursor.connection.commit()
            rest = Restaurant(draft=True)
            created = True
        else:
            rest = Restaurant(**row)
            created = False

        return rest, created

    def list_restaurants(
        self,
        *,
        tags=None,
        metro=None,
        rating=None,
    ) -> list[Restaurant]:
        q = "select * from restaurants"
        params = []

        where_parts = []

        if metro:
            where_parts.append("(metro like ?)")
            params.append(f"%{metro}%")
        if tags:
            where_parts.append(" or ".join("(tags like ?)" for _ in tags))
            params.extend(tags)
        if rating:
            where_parts.append("(rating is null or rating >= ?)")
            params.append(rating)

        if where_parts:
            q = f"{q} where {' AND '.join(where_parts)}"

        rows = self.cursor.execute(q, params).fetchall()
        return [Restaurant(**row) for row in rows]

    def update_draft(self, rest):
        self.cursor.execute(
            """
            update restaurants
            set name         = ?,
                yandex_maps  = ?,
                tags         = ?,
                city         = ?,
                metro        = ?,
                prices       = ?,
                rating       = ?,
                comment      = ?,
                date_created = ?,
                telegram     = ?,
                site         = ?,
                owner        = ?,
                chief        = ?,
                visited      = ?,
                from_channel = ?,
                from_post    = ?,
                draft        = ?
            where draft = 1""",
            (
                rest.get("name", ""),
                rest.get("yandex_maps", ""),
                rest.get("tags", ""),
                rest.get("city", ""),
                rest.get("metro", ""),
                rest.get("prices", ""),
                rest.get("rating", ""),
                rest.get("comment", ""),
                rest.get("date_created", ""),
                rest.get("telegram", ""),
                rest.get("site", ""),
                rest.get("owner", ""),
                rest.get("chief", ""),
                rest.get("visited", ""),
                rest.get("from_channel", ""),
                rest.get("from_post", ""),
                rest.get("draft", ""),
            ),
        )
        self.cursor.connection.commit()

    def get_by_name(self, name: str) -> Restaurant:
        row = self.cursor.execute(
            "select * from restaurants where name = ?", (name,)
        ).fetchone()
        return Restaurant(**row)

    def delete_by_name(self, name: str):
        self.cursor.execute("delete from restaurants where name = ?", (name,))
        self.cursor.connection.commit()

    def check_name_unique(self, name: str) -> bool:
        name = name.strip().lower()
        row = self.cursor.execute(
            "select 1 from restaurants where lower(name) = ?",
            (name,),
        ).fetchone()
        return bool(not row)
