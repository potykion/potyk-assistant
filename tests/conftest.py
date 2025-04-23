import pytest

from kys_in_rest.restaurants.prep.ioc import RestFactory
from tests.cfg import tests_dir


@pytest.fixture()
def rest_factory():
    fact = RestFactory(tests_dir / "test_db.sqlite")
    rest_repo_ = fact.make_sqlite_rest_repo()
    rest_repo_.cursor.execute("delete from restaurants where draft = 1")
    rest_repo_.cursor.connection.commit()

    return fact


@pytest.fixture()
def rest_repo(rest_factory):
    return rest_factory.make_sqlite_rest_repo()
