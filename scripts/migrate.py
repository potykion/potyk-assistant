import os
import sqlite3

import dotenv

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.core.sqlite_utils import apply_migrations

if __name__ == "__main__":
    dotenv.load_dotenv(root_dir / ".env")
    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
    )
    cursor = ioc.resolve(sqlite3.Cursor)
    apply_migrations(cursor)
