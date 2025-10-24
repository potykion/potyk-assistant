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

    def do(self, profile: str) -> None:
        checkins = self.untappd_checkin_scraper.scrape_profile_checkins(profile)
        first_checkin: UntappdCheckin = checkins[0]
        if self.untappd_checkin_repo.checkin_exists(first_checkin.id):
            # no new checkins
            return

        # todo

    def first_time(self, profile: str) -> list[UntappdCheckin]:
        checkins = self.untappd_checkin_scraper.scrape_profile_checkins(profile)
        self.untappd_checkin_repo.insert_checkins(checkins)
        return checkins
