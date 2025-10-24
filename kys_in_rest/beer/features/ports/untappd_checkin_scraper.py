import abc

from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin


class UntappdCheckinScraper:
    @abc.abstractmethod
    def scrape_profile_checkins(self, profile: str) -> list[UntappdCheckin]:
        """Scrape checkins from https://untappd.com/user/{profile}"""
        ...

    @abc.abstractmethod
    def scrape_checkins(
        self, profile: str, init_checkin_id: int
    ) -> list[UntappdCheckin]:
        """Scrape checkins from https://untappd.com/profile/more_feed/{profile}/{init_checkin_id}?v2=true"""
        ...


class UntappdCheckinHtmlLoader:
    @abc.abstractmethod
    def scrape_profile_checkins(self, profile: str) -> str:
        """Get html of https://untappd.com/user/{profile}"""
        ...

    @abc.abstractmethod
    def scrape_checkins(self, profile: str, init_checkin_id: int) -> str:
        """Get html of https://untappd.com/profile/more_feed/{profile}/{init_checkin_id}?v2=true"""
        ...
