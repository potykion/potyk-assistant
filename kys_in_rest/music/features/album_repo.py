import abc

from kys_in_rest.music.entities.album import Album


class AlbumRepo(abc.ABC):
    @abc.abstractmethod
    def list_albums(self) -> list[Album]: ...

    @abc.abstractmethod
    def create_album(self, album: Album) -> Album: ...
