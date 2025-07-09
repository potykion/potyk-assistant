import datetime
import decimal
from typing import Any, cast

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.money.entities.goal import MoneyGoal
from kys_in_rest.money.features.goal_budget import PlanGoalBudgets
from kys_in_rest.money.features.repos.goal_repo import MoneyGoalRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddMoneyGoal(TgFeature):
    def __init__(
        self,
        money_goal_repo: MoneyGoalRepo,
        plan_goal_budgets: PlanGoalBudgets,
    ):
        self.money_goal_repo = money_goal_repo
        self.plan_goal_budgets = plan_goal_budgets

    def do(self, msg: InputTgMsg) -> str | tuple[str, dict[str, Any]]:
        try:
            category, val, date = cast(str, msg.text).split()
        except (ValueError, AttributeError):
            return "Нужно в формате `/mon_goal sport 90000 2025-11-10`"

        goal = MoneyGoal(
            due_date=cast(datetime.date, date),
            val=cast(decimal.Decimal, val),
            category=category,
        )

        self.money_goal_repo.insert(goal)

        budget, *_ = cast(tuple[str, dict[str, Any]], self.plan_goal_budgets.do(msg))

        return (
            f"Записал\n\nБюджеты такие:\n{budget}",
            {"parse_mode": "html"},
        )
