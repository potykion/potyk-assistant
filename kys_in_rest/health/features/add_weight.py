import os
from typing import cast

from kys_in_rest.core.tg_utils import (
    TgFeature,
    SendTgMessageInterrupt,
    TgMsgToSend,
    tg_escape,
)
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddOrShowWeight(TgFeature):
    def __init__(self, weight_repo: WeightRepo):
        self.weight_repo = weight_repo

    def do(self, msg: InputTgMsg) -> str:
        if int(msg.tg_user_id) != int(os.environ["TG_ADMIN"]):
            raise SendTgMessageInterrupt(TgMsgToSend("Тебе нельзя"))

        if msg.text:
            weight = float(msg.text)
            self.weight_repo.add_weight_entry(WeightEntry(weight=weight))
            return "Записал 👌"

        entry = self.weight_repo.get_last()
        if not entry:
            return tg_escape("Нет записей о весе. Добавь через /weight {вес}")

        return tg_escape(f"Последний записанный вес: {entry.weight} кг от {entry.date}")
