from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.beer.features.ports.untappd_checkin_scraper import (
    UntappdCheckinScraper,
)
from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo


class BeerSync:
    def __init__(
        self,
        untappd_checkin_repo: UntappdCheckinRepo,
        untappd_checkin_scraper: UntappdCheckinScraper,
    ):
        self.untappd_checkin_repo = untappd_checkin_repo
        self.untappd_checkin_scraper = untappd_checkin_scraper

    def do(self, profile: str) -> list[UntappdCheckin]:
        all_new_checkins: list[UntappdCheckin] = []

        checkins = self.untappd_checkin_scraper.scrape_profile_checkins(profile)

        while True:
            if existing_ids := self.untappd_checkin_repo.any_checkin_exists(checkins):
                new_checkins = [
                    checkin for checkin in checkins if checkin.id not in existing_ids
                ]
                if not new_checkins:
                    break

                all_new_checkins.extend(new_checkins)
                self.untappd_checkin_repo.insert_checkins(new_checkins)

                if len(new_checkins) == len(checkins):
                    checkins = self.untappd_checkin_scraper.scrape_checkins(
                        profile, new_checkins[-1].id
                    )
                else:
                    break

        return all_new_checkins

    def first_time(self, profile: str) -> list[UntappdCheckin]:
        checkins = self.untappd_checkin_scraper.scrape_profile_checkins(profile)
        self.untappd_checkin_repo.insert_checkins(checkins)
        return checkins


class BeerSyncTg(TgFeature):
    def __init__(self, beer_sync: BeerSync, bot_msg_repo: BotMsgRepo):
        self.beer_sync = beer_sync
        self.bot_msg_repo = bot_msg_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        await self.bot_msg_repo.send_text("Начинаю синхронизацию чекинов...")

        new_checkins = self.beer_sync.do("potykion")
        text = "Чекины синхронизированы"

        if not new_checkins:
            text += ", новых нет"
        else:
            new_checkins_str = "\n".join(
                [
                    f'• <a href="{checkin.beer_url}">{checkin.beer_brewery} — {checkin.beer_name}</a>'
                    for checkin in new_checkins
                ]
            )
            text = f"{text}\n\nНовые чекины:\n{new_checkins_str}"

        await self.bot_msg_repo.send_text(text)
