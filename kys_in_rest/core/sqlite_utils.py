import importlib.util
import os
import sqlite3
import sys

from kys_in_rest.core.cfg import root_dir


def make_sqlite_cursor(db_path: str) -> sqlite3.Cursor:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


class SqliteRepo:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor


def apply_migrations(cursor: sqlite3.Cursor):
    migration_dir = root_dir / "migrations"
    for migration_file in sorted(os.listdir(migration_dir)):
        if not migration_file.endswith(".py"):
            continue
        print(f"Applying migration {migration_file}...")

        migration_file_path = migration_dir / migration_file

        module_name = migration_file_path.stem

        spec = importlib.util.spec_from_file_location(module_name, migration_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        module.migrate(cursor)

        print(f"Applying migration {migration_file}... Done")
