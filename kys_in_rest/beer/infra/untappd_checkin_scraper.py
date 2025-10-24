import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

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
        soup = BeautifulSoup(html, "html.parser")

        # Находим все элементы checkin в #main-stream
        main_stream = soup.select_one("#main-stream")
        if not main_stream:
            return []

        checkin_items = main_stream.select("div.item")
        checkins = [self._parse_checkin_item(item) for item in checkin_items]

        return checkins

    def scrape_checkins(
        self, profile: str, init_checkin_id: int
    ) -> list[UntappdCheckin]:
        html = self.html_loader.scrape_checkins(profile, init_checkin_id)
        soup = BeautifulSoup(html, "html.parser")

        # HTML содержит список div.item элементов
        checkin_items = soup.select("div.item")
        checkins = [self._parse_checkin_item(item) for item in checkin_items]

        return checkins

    def _parse_checkin_item(self, item_div: BeautifulSoup | Tag) -> UntappdCheckin:
        """Парсит отдельный div.item и возвращает UntappdCheckin"""
        # ID из data-checkin-id
        checkin_id = int(item_div.get("data-checkin-id"))

        # Beer URL и изображение
        beer_link = item_div.select_one(".checkin > .top > a.label")
        beer_url = (
            urljoin("https://untappd.com", beer_link.get("href")) if beer_link else ""
        )
        beer_img = beer_link.select_one("img").get("src") if beer_link else ""

        # Парсим текст с информацией о пиве и пивоварне
        text_p = item_div.select_one(".checkin > .top > p.text")
        beer_name = ""
        beer_brewery = ""
        beer_brewery_url = ""
        checkin_location = ""
        checkin_location_url = ""

        if text_p:
            # Извлекаем название пива
            beer_link_in_text = text_p.select_one("a[href*='/b/']")
            if beer_link_in_text:
                beer_name = beer_link_in_text.get_text(strip=True)

            # Извлекаем пивоварню
            brewery_link = text_p.select_one(
                "a[href*='/']:not([href*='/b/']):not([href*='/user/']):not([href*='/v/'])"
            )
            if brewery_link:
                beer_brewery = brewery_link.get_text(strip=True)
                beer_brewery_url = urljoin(
                    "https://untappd.com", brewery_link.get("href")
                )

            # Извлекаем локацию
            venue_link = text_p.select_one("a[href*='/v/']")
            if venue_link:
                checkin_location = venue_link.get_text(strip=True)
                checkin_location_url = urljoin(
                    "https://untappd.com", venue_link.get("href")
                )

        # Комментарий
        comment_div = item_div.select_one(".checkin-comment > p.comment-text")
        checkin_comment = comment_div.get_text(strip=True) if comment_div else ""

        # Рейтинг
        rating_div = item_div.select_one(".caps")
        checkin_rating = float(rating_div.get("data-rating", 0)) if rating_div else 0.0

        # Дата
        time_link = item_div.select_one(".bottom > a.time")
        checkin_date = time_link.get_text(strip=True) if time_link else ""

        return UntappdCheckin(
            id=checkin_id,
            beer_url=beer_url,
            beer_img=beer_img,
            beer_name=beer_name,
            beer_brewery=beer_brewery,
            beer_brewery_url=beer_brewery_url,
            checkin_location=checkin_location,
            checkin_location_url=checkin_location_url,
            checkin_comment=checkin_comment,
            checkin_rating=checkin_rating,
            checkin_date=checkin_date,
        )


class RequestsUntappdCheckinHtmlLoader(UntappdCheckinHtmlLoader):
    def __init__(self, cookie: str, profile="potykion") -> None:
        self.cookie = cookie
        self.headers = {
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

    def scrape_profile_checkins(self, profile: str) -> str:
        url = f"https://untappd.com/user/{profile}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        html = resp.text
        return html

    def scrape_checkins(self, profile: str, init_checkin_id: int) -> str:
        url = (
            f"https://untappd.com/profile/more_feed/{profile}/{init_checkin_id}?v2=true"
        )

        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        html = resp.text
        return html
