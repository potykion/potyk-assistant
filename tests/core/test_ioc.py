from typing import cast

from kys_in_rest.core.ioc import IOC


class MockSqliteCursor:
    def __init__(self, db_path: str):
        self.db_path = db_path


class MockRepo: ...


class _SqliteRepo:
    def __init__(self, cursor: MockSqliteCursor):
        self.cursor = cursor


class MockSqliteRepo(MockRepo, _SqliteRepo): ...


class MockFeature:
    def __init__(self, repo: MockRepo):
        self.repo = repo


def mock_make_sqlite_cursor(db_path: str):
    return MockSqliteCursor(db_path)


def test_ioc(db_path):
    ioc = IOC()
    ioc.register("db_path", db_path)
    ioc.register(MockSqliteCursor, mock_make_sqlite_cursor)
    ioc.register(MockRepo, MockSqliteRepo)
    ioc.register(MockFeature, MockFeature)

    cursor = ioc.resolve(MockSqliteCursor)
    assert cursor.db_path == db_path

    repo = ioc.resolve(MockRepo)
    assert type(repo) is MockSqliteRepo
    assert cast(MockSqliteRepo, repo).cursor.db_path == db_path

    feature = ioc.resolve(MockFeature)
    assert type(feature.repo) is MockSqliteRepo

    new_path = "new" + str(db_path)
    ioc.register("db_path", new_path)
    repo = ioc.resolve(MockRepo)
    assert cast(MockSqliteRepo, repo).cursor.db_path == new_path

def test_ioc_cache(db_path):
    ioc = IOC()
    ioc.register("db_path", db_path)
    ioc.register(MockSqliteCursor, mock_make_sqlite_cursor)

    cursor_1 = ioc.resolve(MockSqliteCursor)
    cursor_2 = ioc.resolve(MockSqliteCursor)
    assert cursor_1 != cursor_2

    ioc.register(MockSqliteCursor, mock_make_sqlite_cursor, cache=True)
    cursor_1 = ioc.resolve(MockSqliteCursor)
    cursor_2 = ioc.resolve(MockSqliteCursor)
    assert cursor_1 == cursor_2

