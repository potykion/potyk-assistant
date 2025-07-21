from kys_in_rest.config.features.load_config import LoadConfig
from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo


class SyncZenMoney(TgFeature):
    def __init__(
        self,
        load_config: LoadConfig,
        bot_msg_repo: BotMsgRepo,
    ):
        self.load_config = load_config
        self.bot_msg_repo = bot_msg_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        config = self.load_config.do()

        await self.bot_msg_repo.send_text("Готово 👌")
