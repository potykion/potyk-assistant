from kys_in_rest.config.entities.config import Config
from kys_in_rest.config.features.load_config import LoadConfig
from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.money.features.repos.zen_money_repo import ZenMoneyRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo


class SyncZenMoney(TgFeature):
    def __init__(
        self,
        load_config: LoadConfig,
        bot_msg_repo: BotMsgRepo,
        zen_money_repo: ZenMoneyRepo,
    ):
        self.load_config = load_config
        self.bot_msg_repo = bot_msg_repo
        self.zen_money_repo = zen_money_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        config: Config = self.load_config.do()

        self.zen_money_repo.sync(server_timestamp=config.zen_money_server_timestamp)

        await self.bot_msg_repo.send_text("Готово 👌")
