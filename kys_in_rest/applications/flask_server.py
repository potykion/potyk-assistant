import os

import dotenv
import flask
from flask import Flask

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.health.features.weight_repo import WeightRepo


def create_app() -> Flask:
    dotenv.load_dotenv(root_dir / ".env")

    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
    )

    app = Flask(__name__)

    @app.route("/weight")
    def weight() -> flask.Response:
        entries = ioc.resolve(WeightRepo).list_weight_entries()
        return flask.jsonify([e.model_dump() for e in entries])

    return app
