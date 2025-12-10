from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.movies.entities.movie import Movie
from kys_in_rest.movies.features.movie_repo import MovieRepo


class SqliteMovieRepo(MovieRepo, SqliteRepo):
    def list_movies(self) -> list[Movie]:
        rows = self.cursor.execute("select * from movies order by id").fetchall()
        return [Movie(**row) for row in rows]

