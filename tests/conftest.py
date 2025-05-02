import os

import pytest

from kys_in_rest.restaurants.prep.ioc import MainFactory
from tests.cfg import tests_dir


@pytest.fixture()
def main_factory():
    fact = MainFactory(tests_dir / "test_db.sqlite")
    rest_repo_ = fact.make_rest_repo()
    fact.sqlite_cursor.execute("delete from restaurants where draft = 1")
    fact.sqlite_cursor.execute("delete from beer_posts")
    fact.sqlite_cursor.connection.commit()
    rest_repo_.delete_by_name(name="test")
    return fact


@pytest.fixture()
def rest_repo(main_factory):
    return main_factory.make_rest_repo()


@pytest.fixture()
def tg_admin_user_id():
    return os.environ.setdefault("TG_ADMIN", "1")
