import sqlite3
import time

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.core.zen_money import ZenMoneyClient, ZenMoneyDiffRaw
from kys_in_rest.money.entities.zen_money import ZenMoneyDiff
from kys_in_rest.money.features.repos.zen_money_repo import ZenMoneyRepo


class SqliteWHttpZenMoneyRepo(SqliteRepo, ZenMoneyRepo):
    def __init__(self, zen_money_client: ZenMoneyClient, cursor: sqlite3.Cursor):
        super().__init__(cursor)
        self.zen_money_client = zen_money_client

    def sync(self, current_client_timestamp: int = None, server_timestamp=0):
        current_client_timestamp = current_client_timestamp or time.time()
        zen_money_diff = self.zen_money_client.diff(
            current_client_timestamp, server_timestamp
        )
        self.save(zen_money_diff)

        return server_timestamp

    def save(self, diff_raw: ZenMoneyDiffRaw):
        server_timestamp = diff_raw["serverTimestamp"]
        current_diff = self.get_current()

        diff = ZenMoneyDiff(server_timestamp=server_timestamp, diff=diff_raw)
        diff_json = diff.model_dump(mode="json")

        if not current_diff:
            self.cursor.execute(
                """insert into zen_money_diff (server_timestamp, diff) values (?, ?)""",
                (diff_json["server_timestamp"], diff_json["diff"]),
            )

    def get_current(self):
        row = self.cursor.execute("select * from zen_money_diff").fetchone()
        return ZenMoneyDiff(**row)
