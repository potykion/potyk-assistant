import sys
import traceback

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.music.features.download_repo import DownloadRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin


class DownloadMusic(TgFeature):
    def __init__(
        self,
        bot_msg_repo: BotMsgRepo,
        check_tg_admin: CheckTgAdmin,
        download_repo: DownloadRepo,
    ):
        self.bot_msg_repo = bot_msg_repo
        self.check_tg_admin = check_tg_admin
        self.download_repo = download_repo

    async def do_async(self, msg: InputTgMsg):
        self.check_tg_admin.do(msg.tg_user_id)

        url = msg.text
        if not url:
            await self.bot_msg_repo.send_text("Че качаем?")
            return

        await self.bot_msg_repo.send_text("Качаю...")

        try:
            audio = self.download_repo.download_audio_from_url(url)
            await self.bot_msg_repo.send_audio(audio)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tr_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            tr = "".join(tr_lines)
            await self.bot_msg_repo.send_text(f"Бля\n{tr}")
