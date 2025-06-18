from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class ShowTgId(TgFeature):
    def do(self, msg: InputTgMsg) -> str:
        return f"Твой id: `{msg.tg_user_id}`"
