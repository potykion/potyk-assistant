from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.beer.features.ports.untappd_checkin_scraper import (
    UntappdCheckinScraper,
)


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
