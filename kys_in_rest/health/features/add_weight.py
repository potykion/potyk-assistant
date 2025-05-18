from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddWeight(TgFeature):
    def __init__(self, weight_repo: WeightRepo):
        self.weight_repo = weight_repo

    def do(self, msg: InputTgMsg) -> str:
        weight = float(msg.text)
        self.weight_repo.add_weight_entry(WeightEntry(weight=weight))
        return "Записал 👌"
