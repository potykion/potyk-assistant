import asyncio
import os
import time
from functools import partial

import dotenv
import schedule
from telegram import Bot

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.tg.infra.bot_msg_repo import TgBotMsgRepo


class SendMedsAlert:
    def __init__(self, bot_msg_repo: BotMsgRepo):
        self.bot_msg_repo = bot_msg_repo

    async def do(self):
        print("lets gooo")
        await self.bot_msg_repo.send_text("test")


def setup():
    dotenv.load_dotenv(root_dir / ".env")

    ioc = make_ioc(
        db_path=str(root_dir / os.environ["DB"]),
        tg_admins=list(map(int, os.environ["TG_ADMINS"].split(","))),
        yandex_music_token=os.environ["YANDEX_MUSIC_TOKEN"],
        zen_money_token=os.environ["ZEN_MONEY_TOKEN"],
    )

    tg_token = os.environ.get("TG_TOKEN")
    tg_admins_str = os.environ.get("TG_ADMINS")
    tg_admins = [int(admin.strip()) for admin in tg_admins_str.split(",")]

    bot = Bot(token=tg_token)

    notification_repo = TgBotMsgRepo(bot, tg_admins)

    ioc.register(BotMsgRepo, notification_repo)

    send_meds_alert = ioc.resolve(SendMedsAlert)

    def do_send_meds_alert():
        asyncio.run(send_meds_alert.do())

    schedule.every(1).seconds.do(do_send_meds_alert)


if __name__ == "__main__":
    print("running cron...")
    setup()
    while True:
        schedule.run_pending()
        time.sleep(1)
