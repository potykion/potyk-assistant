import requests

from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_scraper import (
    UntappdCheckinScraper,
    UntappdCheckinHtmlLoader,
)


class RequestsUntappdCheckinScraper(UntappdCheckinScraper):
    def __init__(
        self,
        cookie: str,
        html_loader: UntappdCheckinHtmlLoader = None,
    ) -> None:
        self.html_loader = html_loader or RequestsUntappdCheckinHtmlLoader(cookie)

    def scrape_profile_checkins(self, profile: str) -> list[UntappdCheckin]:
        html = self.html_loader.scrape_profile_checkins(profile)
        # todo parse html
        #   #main-stream > div.item
        #   = scrape_checkins logic

    def scrape_checkins(
        self, profile: str, init_checkin_id: int
    ) -> list[UntappdCheckin]:
        html = self.html_loader.scrape_checkins(profile, init_checkin_id)
        # todo parse html
        #   html = list of div.item
        #   parse every div to UntappdCheckin
        #   UntappdCheckin(
        #       id=.item data-checkin-id,
        #       beer_url=.checkin > .top > a.label href, + check url starts with https://untappd.com
        #       beer_image_url=.checkin > .top > a.label > img src,
        #       beer_name=...,
        #       brewery_name=...,
        #       brewery_url=...,
        #       brewery_location=...,
        #       brewery_location_url=...,
        #   parse fields below from div.top > p:
        #         <p class="text" data-track-venue-impression="venue_id-12931254-type-checkin_feed">
        #         <a href="/user/potykion" class="user">Никита Лейбович</a> is drinking a <a
        #         href="/b/sabotage-lost-planet-mango-mint-and-passion-fruit/3249068">Lost Planet: Mango, Mint &
        #         Passion Fruit</a> by <a href="/Sabotage_Brewery">Sabotage</a> at <a
        #         href="/v/hophead-pivoteka/12931254">Hophead Pivoteka</a>
        #   </p>
        #       checkin_comment=div.checkin-comment > p.comment-text text,
        #       rating_score= div.caps data-rating,
        #       checkin_time = div.bottom > a.time text,
        #   )


class RequestsUntappdCheckinHtmlLoader(UntappdCheckinHtmlLoader):
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie

    def scrape_profile_checkins(self, profile: str) -> str:
        url = f"https://untappd.com/user/{profile}"
        resp = requests.get(url)
        resp.raise_for_status()
        html = resp.text
        return html

    def scrape_checkins(self, profile: str, init_checkin_id: int) -> str:
        url = (
            f"https://untappd.com/profile/more_feed/{profile}/{init_checkin_id}?v2=true"
        )

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": self.cookie,
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": f"https://untappd.com/user/{profile}",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "YaBrowser";v="25.8", "Yowser";v="2.5"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        html = resp.text
        return html
