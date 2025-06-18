from kys_in_rest.core.tg_utils import (
    TgFeature,
    tg_escape,
)
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.users.features.check_admin import CheckTgAdmin


class AddOrShowWeight(TgFeature):
    def __init__(
        self,
        weight_repo: WeightRepo,
        check_tg_admin: CheckTgAdmin,
    ):
        self.weight_repo = weight_repo
        self.check_tg_admin = check_tg_admin

    def do(self, msg: InputTgMsg) -> str:
        self.check_tg_admin.do(msg.tg_user_id)

        if msg.text:
            weight = float(msg.text)
            self.weight_repo.add_weight_entry(WeightEntry(weight=weight))
            return "Записал 👌"

        entry = self.weight_repo.get_last()
        if not entry:
            return tg_escape("Нет записей о весе. Добавь через /weight {вес}")

        return tg_escape(f"Последний записанный вес: {entry.weight} кг от {entry.date}")
