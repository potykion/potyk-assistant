import os
import sqlite3

import pytest

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.restaurants.features.ports import RestRepo
from tests.cfg import tests_dir


@pytest.fixture()
def db_path():
    return tests_dir / "db_test.sqlite"


@pytest.fixture()
def db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    connection = sqlite3.connect(db_path)
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

    yield db_path

    connection.close()


@pytest.fixture()
def ioc(db):
    ioc_ = make_ioc(db)
    yield ioc_
    ioc_.teardown()


@pytest.fixture()
def rest_repo(ioc):
    return ioc.resolve(RestRepo)


@pytest.fixture()
def tg_admin_user_id():
    return os.environ.setdefault("TG_ADMIN", "1")
