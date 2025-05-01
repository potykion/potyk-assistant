import os

import pytest

from kys_in_rest.restaurants.prep.ioc import RestFactory
from tests.cfg import tests_dir


@pytest.fixture()
def rest_factory():
    fact = RestFactory(tests_dir / "test_db.sqlite")
    rest_repo_ = fact.make_rest_repo()
    rest_repo_.cursor.execute("delete from restaurants where draft = 1")
    rest_repo_.cursor.connection.commit()
    rest_repo_.delete_by_name(name="test")
    return fact


@pytest.fixture()
def rest_repo(rest_factory):
    return rest_factory.make_rest_repo()

@pytest.fixture()
def tg_admin_user_id():
    return os.environ.setdefault("TG_ADMIN", "1")
