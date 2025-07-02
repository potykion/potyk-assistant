import decimal
from typing import Any, cast

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.money.entities.spending import Spending
from kys_in_rest.money.features.spending_repo import SpendingRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddSpending(TgFeature):
    def __init__(self, spending_repo: SpendingRepo):
        self.spending_repo = spending_repo

    def do(self, msg: InputTgMsg) -> str | tuple[str, dict[str, Any]]:
        text = cast(str, msg.text)
        if not text:
            spendings = self.spending_repo.list_today()
            if not spendings:
                return "Сегодня трат нет"

            return "Траты за день:\n".join(
                f"• {spending.comment} - {spending.amount}" for spending in spendings
            )

        try:
            amount, comment = text.split()
        except (ValueError, AttributeError):
            return "Нужно прислать в формате `/spend 100 пятерка`"

        spending = Spending(
            amount=decimal.Decimal(amount),
            comment=comment,
        )
        self.spending_repo.add_spending(spending)
        return "Записал 👌"
