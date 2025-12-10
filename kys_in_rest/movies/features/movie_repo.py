import abc

from kys_in_rest.movies.entities.movie import Movie


class MovieRepo(abc.ABC):
    @abc.abstractmethod
    def list_movies(self) -> list[Movie]: ...

    @abc.abstractmethod
    def create_movie(self, movie: Movie) -> Movie: ...

    @abc.abstractmethod
    def update_movie(self, movie: Movie) -> None: ...

    @abc.abstractmethod
    def get_by_id(self, movie_id: int) -> Movie | None: ...

