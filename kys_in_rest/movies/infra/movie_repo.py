from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.movies.entities.movie import Movie
from kys_in_rest.movies.features.movie_repo import MovieRepo


class SqliteMovieRepo(MovieRepo, SqliteRepo):
    def list_movies(self) -> list[Movie]:
        rows = self.cursor.execute("select * from movies order by id").fetchall()
        return [Movie(**row) for row in rows]

    def create_movie(self, movie: Movie) -> Movie:
        self.cursor.execute(
            """
            insert into movies (title, image, kinopoisk_url, download_url, watch_url, why)
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                movie.title,
                movie.image,
                movie.kinopoisk_url,
                movie.download_url,
                movie.watch_url,
                movie.why,
            ),
        )
        self.cursor.connection.commit()
        movie_id = self.cursor.lastrowid
        return Movie(id=movie_id, **movie.model_dump(exclude={"id"}))

    def update_movie(self, movie: Movie) -> None:
        if movie.id is None:
            raise ValueError("Movie id is required for update")
        self.cursor.execute(
            """
            update movies
            set title = ?, image = ?, kinopoisk_url = ?, download_url = ?, watch_url = ?, why = ?
            where id = ?
            """,
            (
                movie.title,
                movie.image,
                movie.kinopoisk_url,
                movie.download_url,
                movie.watch_url,
                movie.why,
                movie.id,
            ),
        )
        self.cursor.connection.commit()

    def get_by_id(self, movie_id: int) -> Movie | None:
        row = self.cursor.execute("select * from movies where id = ?", (movie_id,)).fetchone()
        if not row:
            return None
        return Movie(**row)

