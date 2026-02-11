import sqlite3

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.music.entities.album import Album
from kys_in_rest.music.features.album_repo import AlbumRepo
from kys_in_rest.tags.features.tag_repo import TagRepo


class SqliteAlbumRepo(AlbumRepo, SqliteRepo):
    def __init__(self, cursor: sqlite3.Cursor, tag_repo: TagRepo) -> None:
        SqliteRepo.__init__(self, cursor)
        self.tag_repo = tag_repo

    def list_albums(self) -> list[Album]:
        rows = self.cursor.execute("select * from mu_album order by id").fetchall()
        return [
            Album(**{**dict(row), "tags": self.tag_repo.get_tag_ids_for_entity(row["id"], "mu_album")})
            for row in rows
        ]

    def create_album(self, album: Album) -> Album:
        self.cursor.execute(
            """
            insert into mu_album (title, artist, year, cover, link)
            values (?, ?, ?, ?, ?)
            """,
            (
                album.title,
                album.artist,
                album.year,
                album.cover,
                album.link,
            ),
        )
        self.cursor.connection.commit()
        album_id = self.cursor.lastrowid
        if album_id is None:
            raise ValueError("Failed to get album id after insert")
        self.tag_repo.set_tags_for_entity(album_id, "mu_album", album.tags)
        return Album(id=album_id, **album.model_dump(exclude={"id"}))

    def update_album(self, album: Album) -> None:
        if album.id is None:
            raise ValueError("Album id is required for update")
        album_id = album.id
        self.cursor.execute(
            """
            update mu_album
            set title = ?, artist = ?, year = ?, cover = ?, link = ?
            where id = ?
            """,
            (
                album.title,
                album.artist,
                album.year,
                album.cover,
                album.link,
                album_id,
            ),
        )
        self.cursor.connection.commit()
        self.tag_repo.set_tags_for_entity(album_id, "mu_album", album.tags)

    def get_by_id(self, album_id: int) -> Album | None:
        row = self.cursor.execute("select * from mu_album where id = ?", (album_id,)).fetchone()
        if not row:
            return None
        album_dict = dict(row)
        album_dict["tags"] = self.tag_repo.get_tag_ids_for_entity(album_id, "mu_album")
        return Album(**album_dict)
