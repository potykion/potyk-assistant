import importlib.util
import os
import sqlite3
import sys
from pathlib import Path
from types import ModuleType

from kys_in_rest.core.cfg import root_dir


def make_sqlite_cursor(db_path: str) -> sqlite3.Cursor:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


class SqliteRepo:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor


def apply_migrations(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
    create table if not exists migrations
    (
        migration TEXT
    );
    """
    )
    cursor.connection.commit()

    migration_dir = root_dir / "migrations"
    for migration_file in sorted(os.listdir(migration_dir)):
        if not migration_file.endswith(".py"):
            continue
        print(f"Applying migration {migration_file}...")

        migration_file_path = migration_dir / migration_file

        module_name = migration_file_path.stem
        applied = cursor.execute(
            "select 1 from migrations where migration = ?", (module_name,)
        ).fetchone()
        if applied:
            print(f"Applying migration {migration_file}... Already applied")
            continue

        module = _compile_migration(module_name, migration_file_path)
        if not module:
            print(f"Applying migration {migration_file}... Migration is broken/invalid")
            break

        module.migrate(cursor)

        print(f"Applying migration {migration_file}... Done")

        cursor.execute("insert into migrations (migration) values (?)", (module_name,))
        cursor.connection.commit()


def _compile_migration(
    module_name: str,
    migration_file_path: Path | str,
) -> ModuleType | None:
    spec = importlib.util.spec_from_file_location(module_name, migration_file_path)
    if not spec:
        return None
    module = importlib.util.module_from_spec(spec)
    if not module:
        return None
    sys.modules[module_name] = module
    loader = spec.loader
    if not loader:
        return None
    loader.exec_module(module)
    return module
