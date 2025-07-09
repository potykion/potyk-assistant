import datetime
import math
from itertools import groupby
from typing import Generator, Any

from dateutil.relativedelta import relativedelta

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.money.entities.goal import MoneyGoal
from kys_in_rest.money.features.repos.goal_repo import MoneyGoalRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class PlanGoalBudgets(TgFeature):
    def __init__(self, money_goal_repo: MoneyGoalRepo):
        self.money_goal_repo = money_goal_repo

    def do(self, msg: InputTgMsg) -> str | tuple[str, dict[str, Any]]:
        goals: list[MoneyGoal] = self.money_goal_repo.list_actual()

        messages = []

        for category, per_month in self._compute_per_month_by_category(goals):
            messages.append(f"• {category=}: {per_month=}")

        return "\n".join(messages), {"parse_mode": "html"}

    @classmethod
    def _compute_per_month_by_category(
        cls, goals: list[MoneyGoal], now: datetime.date = None
    ) -> Generator[tuple[str, int], None, None]:
        """
        >>> list(
        ...     PlanGoalBudgets._compute_per_month_by_category(
        ...         [
        ...             MoneyGoal(due_date=datetime.date(2025,11,10), val=90_000, category="sport"),
        ...             MoneyGoal(due_date=datetime.date(2025,8,14), val=40_000, category="sport"),
        ...         ],
        ...         now=datetime.date(2025, 7, 9),
        ...     )
        ... )
        [('sport', 62500)]
        """
        now = now or datetime.date.today()
        all_cat_goals = groupby(goals, lambda g: g.category)
        for category, cat_goals in all_cat_goals:
            per_month = 0
            for goal in cat_goals:
                months = max(relativedelta(goal.due_date, now).months, 1)
                per_month += math.ceil(goal.val / months)

            yield category, per_month
