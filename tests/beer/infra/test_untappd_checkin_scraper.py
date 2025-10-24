import re

import pytest
from pathlib import Path

from kys_in_rest.beer.infra.untappd_checkin_scraper import (
    RequestsUntappdCheckinScraper,
    UntappdCheckinHtmlLoader,
)


@pytest.fixture()
def html_loader():
    base = Path(__file__).parent
    profile_html = (base / "untappd_checkins_profile.html").read_text(encoding="utf-8")
    more_html = (base / "untappd_checkins_more.html").read_text(encoding="utf-8")

    class MockLoader(UntappdCheckinHtmlLoader):
        def scrape_profile_checkins(self, *args, **kwargs):
            return profile_html

        def scrape_checkins(self, *args, **kwargs):
            return more_html

    return MockLoader()


@pytest.fixture()
def scraper(html_loader):
    return RequestsUntappdCheckinScraper("", html_loader)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def test_RequestsUntappdCheckinScraper_scrape_profile_checkins(scraper):
    checkins = scraper.scrape_profile_checkins("potykion")
    assert len(checkins) == 2

    assert checkins[0].id == 1523173734
    assert checkins[0].beer_url == "https://untappd.com/b/paradox-pumpkin-hell/6415786"
    assert (
        checkins[0].beer_img
        == "https://assets.untappd.com/site/beer_logos/beer-6415786_070c5_sm.jpeg"
    )
    assert checkins[0].beer_name == "PUMPKIN HELL"
    assert checkins[0].beer_brewery == "Paradox"
    assert checkins[0].beer_brewery_url == "https://untappd.com/paradox-beer"
    assert checkins[0].checkin_location == "Share House"
    assert (
        checkins[0].checkin_location_url == "https://untappd.com/v/share-house/7728362"
    )
    assert (
        normalize_spaces(checkins[0].checkin_comment.strip())
        == "Крч все дороги ведут в Шер По традиции тестим новые тыковки Спайсово, остренько, с лёгким дымком Имеет место быть 🌶️"
    )
    assert checkins[0].checkin_rating == 3.75
    assert (
        normalize_spaces(checkins[0].checkin_date) == "Thu, 23 Oct 2025 19:34:24 +0000"
    )


def test_RequestsUntappdCheckinScraper_scrape_checkins(scraper):
    checkins = scraper.scrape_checkins("potykion", 1234567890)
    assert len(checkins) == 2

    assert checkins[0].id == 1523079395
    assert (
        checkins[0].beer_url
        == "https://untappd.com/b/sabotage-lost-planet-mango-mint-and-passion-fruit/3249068"
    )
    assert (
        checkins[0].beer_img
        == "https://assets.untappd.com/site/beer_logos/beer-3249068_db5c0_sm.jpeg"
    )
    assert (
        normalize_spaces(checkins[0].beer_name)
        == "Lost Planet: Mango, Mint & Passion Fruit"
    )
    assert checkins[0].beer_brewery == "Sabotage"
    assert checkins[0].beer_brewery_url == "https://untappd.com/Sabotage_Brewery"
    assert checkins[0].checkin_location == "Hophead Pivoteka"
    assert (
        checkins[0].checkin_location_url
        == "https://untappd.com/v/hophead-pivoteka/12931254"
    )
    assert (
        normalize_spaces(checkins[0].checkin_comment)
        == "Пора переходить на нормальное пиво, а то уже холодно Очень освежающий и прохладный. Мята яркая и дерзкая, манго базовое, но хорошо оттеняет. Да нормально так то, только и правда уже не сезон🌧️🌧️🌧️"
    )
    assert checkins[0].checkin_rating == 4.25
    assert checkins[0].checkin_date == "Thu, 23 Oct 2025 08:55:39 +0000"
