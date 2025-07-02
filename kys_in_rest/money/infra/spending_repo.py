from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.money.entities.spending import Spending
from kys_in_rest.money.features.spending_repo import SpendingRepo


class SqliteSpendingRepo(SqliteRepo, SpendingRepo):
    def add_spending(self, spending: Spending) -> None:
        self.cursor.execute(
            "insert into spendings (created_dt, amount, comment) values (?, ?, ?)",
            (
                spending.created_dt,
                spending.amount,
                spending.comment,
            ),
        )
        self.cursor.connection.commit()
