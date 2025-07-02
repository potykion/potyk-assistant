from datetime import datetime

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.money.entities.spending import Spending
from kys_in_rest.money.features.spending_repo import SpendingRepo


class SqliteSpendingRepo(SqliteRepo, SpendingRepo):
    def add_spending(self, spending: Spending) -> None:
        sql_spending = spending.model_dump(mode="json")
        self.cursor.execute(
            "insert into spendings (created_dt, amount, comment) values (?, ?, ?)",
            (
                sql_spending["created_dt"],
                sql_spending["amount"],
                sql_spending["comment"],
            ),
        )
        self.cursor.connection.commit()

    def list_today(self, now=None):
        now = now or datetime.now()
        self.cursor.execute(
            "select * from spendings where date(created_dt) = ?",
            (now.date(),),
        )
        spendings = self.cursor.fetchall()
        return [Spending(**spending) for spending in spendings]
