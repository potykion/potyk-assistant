import datetime

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.money.entities.goal import MoneyGoal
from kys_in_rest.money.features.repos.goal_repo import MoneyGoalRepo


class SqliteMoneyGoalRepo(SqliteRepo, MoneyGoalRepo):
    def list_actual(self, now: datetime.date = None) -> list[MoneyGoal]:
        now = now or datetime.date.today()
        rows = self.cursor.execute(
            "SELECT * FROM mon_goals where date(due_date) > ? ",
            (now,),
        )
        return [MoneyGoal(**row) for row in rows]

    def insert(self, goal: MoneyGoal):
        goal_dict = goal.model_dump(mode="json")
        self.cursor.execute(
            "INSERT  INTO mon_goals (due_date, val, category) VALUES (?, ?, ?)",
            (goal_dict["due_date"], goal_dict["val"], goal_dict["category"]),
        )
        self.cursor.connection.commit()
