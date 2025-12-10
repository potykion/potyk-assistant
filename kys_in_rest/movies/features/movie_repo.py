import abc

from kys_in_rest.movies.entities.movie import Movie


class MovieRepo(abc.ABC):
    @abc.abstractmethod
    def list_movies(self) -> list[Movie]: ...

