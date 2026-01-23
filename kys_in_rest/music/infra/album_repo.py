from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.music.entities.album import Album
from kys_in_rest.music.features.album_repo import AlbumRepo


class SqliteAlbumRepo(AlbumRepo, SqliteRepo):
    def list_albums(self) -> list[Album]:
        rows = self.cursor.execute("select * from mu_album order by id").fetchall()
        return [Album(**dict(row)) for row in rows]

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
        return Album(id=album_id, **album.model_dump(exclude={"id"}))

    def update_album(self, album: Album) -> None:
        if album.id is None:
            raise ValueError("Album id is required for update")
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
                album.id,
            ),
        )
        self.cursor.connection.commit()

    def get_by_id(self, album_id: int) -> Album | None:
        row = self.cursor.execute("select * from mu_album where id = ?", (album_id,)).fetchone()
        if not row:
            return None
        return Album(**dict(row))
