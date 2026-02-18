import abc

from kys_in_rest.music.entities.album import Album


class AlbumRepo(abc.ABC):
    @abc.abstractmethod
    def list_albums(self) -> list[Album]: ...

    @abc.abstractmethod
    def create_album(self, album: Album) -> Album: ...

    @abc.abstractmethod
    def update_album(self, album: Album) -> None: ...

    @abc.abstractmethod
    def get_by_id(self, album_id: int) -> Album | None: ...
