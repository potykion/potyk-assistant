from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.tags.entities.tag import Tag
from kys_in_rest.tags.features.tag_repo import TagRepo


class SqliteTagRepo(TagRepo, SqliteRepo):
    def list_tags(self, entity_type: str | None = None) -> list[Tag]:
        if entity_type:
            rows = self.cursor.execute(
                "select * from tags where entity_type = ? order by title",
                (entity_type,),
            ).fetchall()
        else:
            rows = self.cursor.execute("select * from tags order by title").fetchall()
        return [Tag(**dict(row)) for row in rows]

    def get_tag_ids_for_entity(self, entity_id: int, entity_type: str) -> list[int]:
        rows = self.cursor.execute(
            "select tag_id from tag_m2m where entity_id = ? and entity_type = ?",
            (entity_id, entity_type),
        ).fetchall()
        return [row["tag_id"] for row in rows]

    def set_tags_for_entity(self, entity_id: int, entity_type: str, tag_ids: list[int]) -> None:
        self.cursor.execute(
            "delete from tag_m2m where entity_id = ? and entity_type = ?",
            (entity_id, entity_type),
        )
        for tag_id in tag_ids:
            self.cursor.execute(
                "insert into tag_m2m (tag_id, entity_id, entity_type) values (?, ?, ?)",
                (tag_id, entity_id, entity_type),
            )
        self.cursor.connection.commit()
