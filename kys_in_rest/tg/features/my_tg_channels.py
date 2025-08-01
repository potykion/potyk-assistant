from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.tg.features.repos.my_tg_channels_repo import MyTgChannelsRepo


class ListMyTgChannels(TgFeature):
    def __init__(
        self,
        my_tg_channels_repo: MyTgChannelsRepo,
        bot_msg_repo: BotMsgRepo,
    ):
        self.my_tg_channels_repo = my_tg_channels_repo
        self.bot_msg_repo = bot_msg_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        channels = self.my_tg_channels_repo.list()

        channels_str = "\n".join(
            f'• <a href="{channel.link}">{channel.name}</a>' for channel in channels
        )
        channels_msg = f"""<b>КАНАЛЫ МОИ</b>\n\n{channels_str}"""
        await self.bot_msg_repo.send_text(channels_msg)
