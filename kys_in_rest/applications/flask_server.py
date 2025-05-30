import os

import dotenv
import flask
from flask import Flask

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.health.features.weight_repo import WeightRepo

dotenv.load_dotenv()

ioc = make_ioc(str(root_dir / os.environ["DB"]))

app = Flask(__name__)


@app.route("/weight")
def weight():
    entries = ioc.resolve(WeightRepo).list_weight_entries()
    return flask.jsonify([e.model_dump() for e in entries])
