from kys_in_rest.core.tg_utils import TgFeature, tg_escape
from kys_in_rest.tg.entities.command import TgCommandSetup
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class Help(TgFeature):
    def __init__(self, tg_commands: list[TgCommandSetup]):
        self.tg_commands = tg_commands

    def do(self, msg: InputTgMsg) -> str | tuple[str, dict]:
        msg = "\n".join(tg_escape(f"• /{tg_command.command} — {tg_command.desc}") for tg_command in self.tg_commands)
        msg = f"<b>Вот что умеет бот:</b>\n{msg}"
        return msg, {"parse_mode": "html"}
