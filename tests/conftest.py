import os
import sqlite3

import pytest

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.sqlite_utils import apply_migrations
from kys_in_rest.restaurants.features.ports import RestRepo
from tests.cfg import tests_dir


@pytest.fixture()
def db_path():
    return tests_dir / "db_test.sqlite"


@pytest.fixture()
def tg_admin_user_id():
    return 1


@pytest.fixture()
def ioc(db_path, tg_admin_user_id):
    if os.path.exists(db_path):
        os.remove(db_path)

    ioc_ = make_ioc(
        db_path=db_path,
        tg_admins=[tg_admin_user_id],
        yandex_music_token="no",
    )

    cursor = ioc_.resolve(sqlite3.Cursor)
    apply_migrations(cursor)

    yield ioc_
    ioc_.teardown()


@pytest.fixture()
def rest_repo(ioc):
    return ioc.resolve(RestRepo)
