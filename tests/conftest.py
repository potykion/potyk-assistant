import os
import sqlite3

import pytest

from kys_in_rest.restaurants.prep.ioc import MainFactory
from tests.cfg import tests_dir


@pytest.fixture()
def db():
    test_db = tests_dir / "db_test.sqlite"
    if os.path.exists(test_db):
        os.remove(test_db)
    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE "beer_posts"
        (
            created TEXT,
            beers   text,
            id      integer not null
                constraint beer_posts_pk
                    primary key autoincrement
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE flow
        (
            command TEXT
            , tg_user_id integer);
        """
    )
    cursor.execute(
        """
        CREATE TABLE "restaurants"
        (
            name         TEXT,
            yandex_maps  TEXT,
            tags         TEXT,
            city         TEXT,
            metro        TEXT,
            prices       TEXT,
            rating       INTEGER,
            comment      TEXT,
            date_created TEXT,
            telegram     TEXT,
            site         TEXT,
            owner        TEXT,
            chief        TEXT,
            visited      integer,
            from_channel TEXT,
            from_post    TEXT
            , draft integer);
        """
    )
    connection.commit()

    yield test_db

    connection.close()


@pytest.fixture()
def main_factory(db):
    factory = MainFactory(db)
    yield factory
    factory.teardown()



@pytest.fixture()
def rest_repo(main_factory):
    return main_factory.make_rest_repo()


@pytest.fixture()
def tg_admin_user_id():
    return os.environ.setdefault("TG_ADMIN", "1")
