from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.beer.features.ports.untappd_checkin_scraper import (
    UntappdCheckinScraper,
)
from kys_in_rest.core.date_utils import (
    get_month_ago_moscow,
    get_week_ago_moscow,
    get_yesterday_moscow,
    is_checkin_in_period,
)
from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin


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
            existing_ids = self.untappd_checkin_repo.any_checkin_exists(checkins)
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

    def get_stats(self) -> dict[str, int]:
        """Возвращает статистику по выпитому пиву за разные периоды."""
        all_checkins = self.untappd_checkin_repo.get_checkins_since(
            get_month_ago_moscow()
        )
        
        yesterday_start = get_yesterday_moscow()
        week_ago = get_week_ago_moscow()
        month_ago = get_month_ago_moscow()
        
        yesterday_count = sum(
            1 for checkin in all_checkins
            if is_checkin_in_period(checkin.checkin_date, yesterday_start)
        )
        
        week_count = sum(
            1 for checkin in all_checkins
            if is_checkin_in_period(checkin.checkin_date, week_ago)
        )
        
        month_count = sum(
            1 for checkin in all_checkins
            if is_checkin_in_period(checkin.checkin_date, month_ago)
        )
        
        return {
            "yesterday": yesterday_count,
            "week": week_count,
            "month": month_count,
        }


class BeerSyncTg(TgFeature):
    def __init__(
        self,
        beer_sync: BeerSync,
        bot_msg_repo: BotMsgRepo,
        check_tg_admin: CheckTgAdmin,
    ):
        self.beer_sync = beer_sync
        self.bot_msg_repo = bot_msg_repo
        self.check_tg_admin = check_tg_admin

    async def do_async(self, msg: InputTgMsg) -> None:
        self.check_tg_admin.do(msg.tg_user_id)

        await self.bot_msg_repo.send_text("Начинаю синхронизацию чекинов...")

        new_checkins = self.beer_sync.do("potykion")
        stats = self.beer_sync.get_stats()
        
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

        # Добавляем статистику
        stats_text = f"\n\n📊 Статистика:\n"
        stats_text += f"• Вчера: {stats['yesterday']} пива\n"
        stats_text += f"• За неделю: {stats['week']} пива\n"
        stats_text += f"• За месяц: {stats['month']} пива"
        
        text += stats_text

        await self.bot_msg_repo.send_text(text)
