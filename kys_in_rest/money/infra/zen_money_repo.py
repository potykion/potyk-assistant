import datetime
import json
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

    def sync(
        self, current_client_timestamp: int | None = None, server_timestamp: int = 0
    ) -> int:
        current_client_timestamp = current_client_timestamp or int(time.time())
        zen_money_diff = self.zen_money_client.diff(
            current_client_timestamp, server_timestamp
        )
        self.save(zen_money_diff)

        return server_timestamp

    def save(self, diff_raw: ZenMoneyDiffRaw) -> None:
        server_timestamp = diff_raw["serverTimestamp"]
        current_diff = self.get_current()

        diff = ZenMoneyDiff(server_timestamp=server_timestamp, diff=diff_raw)
        diff_json = diff.model_dump(mode="json")

        if not current_diff:
            self.cursor.execute(
                """insert into zen_money_diff (server_timestamp, diff) values (?, ?)""",
                (diff_json["server_timestamp"], json.dumps(diff_json["diff"])),
            )
            self.cursor.connection.commit()
        else:
            # todo apply diff
            ...

    def get_current(self) -> ZenMoneyDiff | None:
        row = self.cursor.execute("select * from zen_money_diff").fetchone()
        if not row:
            return None
        return ZenMoneyDiff(
            server_timestamp=row["server_timestamp"],
            diff=json.loads(row["diff"]),
        )

    def monthly_spent(self, current_date: datetime.date=None) -> float:
        current_date = current_date or datetime.date.today()
        current_date = datetime.date(current_date.year, current_date.month, 1)

        sql = """
              SELECT SUM(
                             CAST(json_extract(value, '$.outcome') AS REAL)
                     )

              FROM zen_money_diff, json_each(json_extract(diff, '$.transaction'))
              where json_extract(value, '$.deleted') is false
                and date(json_extract(value, '$.date')) >= ?
                and cast(json_extract(value, '$.outcome') AS REAL) != CAST(json_extract(value, '$.income') AS REAL)

              order by json_extract(value, '$.date')
              """
        result = self.cursor.execute(sql, (current_date,)).fetchone()
        return result[0] if result and result[0] is not None else 0.0
