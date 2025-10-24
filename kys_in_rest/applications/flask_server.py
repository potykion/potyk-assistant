import os

import dotenv
import flask
from flask import Flask

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.beer.features.beer_sync import BeerSync
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.health.features.weight_repo import WeightRepo


def create_app() -> Flask:
    dotenv.load_dotenv(root_dir / ".env")

    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
        yandex_music_token=os.environ["YANDEX_MUSIC_TOKEN"],
        zen_money_token=os.environ["ZEN_MONEY_TOKEN"],
    )

    app = Flask(__name__)

    @app.route("/weight")
    def weight() -> flask.Response:
        entries = ioc.resolve(WeightRepo).list_weight_entries()
        return flask.jsonify([e.model_dump() for e in entries])

    # todo auth required
    @app.route("/beer/sync", methods=["POST"])
    def beer_sync() -> flask.Response: ...

    @app.route("/beer/sync_first_time", methods=["POST"])
    def beer_sync_first_time() -> flask.Response:
        beer_sync = ioc.resolve(BeerSync)
        checkins = beer_sync.first_time("potykion")
        return flask.jsonify([c.model_dump() for c in checkins])

    return app
