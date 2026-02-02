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
