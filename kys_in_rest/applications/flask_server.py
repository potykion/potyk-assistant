import os

import dotenv
import flask
from flask import Flask
from flask_cors import CORS

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.beer.features.beer_sync import BeerSync
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.movies.features.movie_repo import MovieRepo


def create_app() -> Flask:
    dotenv.load_dotenv(root_dir / ".env")

    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
        yandex_music_token=os.environ["YANDEX_MUSIC_TOKEN"],
        zen_money_token=os.environ["ZEN_MONEY_TOKEN"],
        untappd_cookie=os.environ["UNTAPPD_COOKIE"],
    )

    app = Flask(__name__)
    CORS(app)

    @app.route("/weight")
    def weight() -> flask.Response:
        entries = ioc.resolve(WeightRepo).list_weight_entries()
        return flask.jsonify([e.model_dump() for e in entries])

    @app.route("/movies")
    def movies() -> flask.Response:
        movies_list = ioc.resolve(MovieRepo).list_movies()
        return flask.jsonify([m.model_dump() for m in movies_list])

    @app.route("/movies", methods=["POST"])
    def create_movie() -> tuple[flask.Response, int]:
        movie_repo = ioc.resolve(MovieRepo)
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        from kys_in_rest.movies.entities.movie import Movie

        movie = Movie(**data)
        created_movie = movie_repo.create_movie(movie)
        return flask.jsonify(created_movie.model_dump()), 201

    @app.route("/movies/<int:movie_id>", methods=["PUT"])
    def update_movie(movie_id: int) -> tuple[flask.Response, int]:
        movie_repo = ioc.resolve(MovieRepo)
        existing_movie = movie_repo.get_by_id(movie_id)
        if not existing_movie:
            return flask.jsonify({"error": "Movie not found"}), 404

        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        from kys_in_rest.movies.entities.movie import Movie

        movie = Movie(id=movie_id, **data)
        movie_repo.update_movie(movie)
        updated_movie = movie_repo.get_by_id(movie_id)
        return flask.jsonify(updated_movie.model_dump() if updated_movie else {}), 200

    # todo auth required
    @app.route("/beer/sync", methods=["POST"])
    def beer_sync() -> flask.Response:
        beer_sync = ioc.resolve(BeerSync)
        checkins = beer_sync.do("potykion")
        return flask.jsonify([c.model_dump() for c in checkins])

    @app.route("/beer/sync_first_time", methods=["POST"])
    def beer_sync_first_time() -> flask.Response:
        beer_sync = ioc.resolve(BeerSync)
        checkins = beer_sync.first_time("potykion")
        return flask.jsonify([c.model_dump() for c in checkins])

    @app.route("/auth/telegram", methods=["POST"])
    def auth_telegram() -> flask.Response:
        data = flask.request.get_json()
        if not data:
            return flask.jsonify({"error": "No JSON data provided"}), 400

        tg_user_id = data.get("id")
        if not tg_user_id:
            return flask.jsonify({"error": "Telegram user ID is required"}), 400

        tg_admins = ioc.resolve("tg_admins")
        is_admin = int(tg_user_id) in tg_admins

        return flask.jsonify({
            "user": data,
            "is_admin": is_admin,
        }), 200

    return app
