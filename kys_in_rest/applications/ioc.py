import sqlite3
from typing import Sequence

from kys_in_rest.beer.features.ports.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.beer.features.ports.untappd_checkin_scraper import (
    UntappdCheckinScraper,
)
from kys_in_rest.beer.infra.beer_post_repo import SqliteBeerPostRepo
from kys_in_rest.beer.infra.untappd_checkin_repo import SqliteUntappdCheckinRepo
from kys_in_rest.beer.infra.untappd_checkin_scraper import RequestsUntappdCheckinScraper
from kys_in_rest.config.features.repos.config_repo import ConfigRepo
from kys_in_rest.config.infra.config_repo import SqliteConfigRepo
from kys_in_rest.core.ioc import IOC
from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.health.infra.weight_repo import SqliteWeightRepo
from kys_in_rest.movies.features.movie_repo import MovieRepo
from kys_in_rest.movies.infra.movie_repo import SqliteMovieRepo
from kys_in_rest.money.features.repos.goal_repo import MoneyGoalRepo
from kys_in_rest.money.features.repos.spending_repo import SpendingRepo
from kys_in_rest.money.features.repos.tinkoff_candles_repo import TinkoffCandlesRepo
from kys_in_rest.money.features.repos.zen_money_repo import ZenMoneyRepo
from kys_in_rest.money.infra.goal_repo import SqliteMoneyGoalRepo
from kys_in_rest.money.infra.spending_repo import SqliteSpendingRepo
from kys_in_rest.money.infra.tinkoff_candles_repo import TinkoffInvestCandlesRepo
from kys_in_rest.money.infra.zen_money_repo import SqliteWHttpZenMoneyRepo
from kys_in_rest.music.features.album_repo import AlbumRepo
from kys_in_rest.music.features.download_repo import DownloadRepo
from kys_in_rest.music.infra.album_repo import SqliteAlbumRepo
from kys_in_rest.music.infra.download_repo import (
    UrlDownloadRepo,
    YandexMusicDownloadRepo,
    YouTubeDownloadRepo,
)
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tags.features.tag_repo import TagRepo
from kys_in_rest.tags.infra.tag_repo import SqliteTagRepo
from kys_in_rest.tg.entities.command import TgCommandSetup
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.features.repos.my_tg_channels_repo import MyTgChannelsRepo
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo
from kys_in_rest.tg.infra.my_tg_channels_repo import SqliteMyTgChannelsRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin
from kys_in_rest.wishlist.features.ports.wishlist_repo import WishlistRepo
from kys_in_rest.wishlist.infra.wishlist_repo import SqliteWishlistRepo


def make_ioc(
    *,
    db_path: str,
    tg_admins: list[int],
    tg_commands: Sequence[TgCommandSetup] = (),
    yandex_music_token: str,
    zen_money_token: str,
    tinkoff_invest_token: str = "",
    untappd_cookie: str = "",
) -> IOC:
    ioc = IOC()

    # deps
    ioc.register("db_path", db_path)
    ioc.register("zen_money_token", zen_money_token)
    ioc.register("tinkoff_invest_token", tinkoff_invest_token)
    ioc.register("tg_admins", tg_admins)
    ioc.register("tg_commands", tg_commands)
    ioc.register(
        sqlite3.Cursor,
        make_sqlite_cursor,
        cache=True,
        teardown=lambda cursor: cursor.connection.close(),
    )

    # ports
    ioc.register(RestRepo, SqliteRestRepo)
    ioc.register(FlowRepo, SqliteFlowRepo)
    ioc.register(BeerPostRepo, SqliteBeerPostRepo)
    ioc.register(WeightRepo, SqliteWeightRepo)
    ioc.register(MovieRepo, SqliteMovieRepo)
    ioc.register(AlbumRepo, SqliteAlbumRepo)
    ioc.register(TagRepo, SqliteTagRepo)
    ioc.register(WishlistRepo, SqliteWishlistRepo)
    ioc.register(SpendingRepo, SqliteSpendingRepo)
    ioc.register(MoneyGoalRepo, SqliteMoneyGoalRepo)
    ioc.register(ConfigRepo, SqliteConfigRepo)
    ioc.register(
        DownloadRepo,
        lambda: UrlDownloadRepo(
            YandexMusicDownloadRepo(yandex_music_token),
            YouTubeDownloadRepo(),
        ),
    )
    ioc.register(ZenMoneyRepo, SqliteWHttpZenMoneyRepo)
    ioc.register(MyTgChannelsRepo, SqliteMyTgChannelsRepo)

    ioc.register(UntappdCheckinRepo, SqliteUntappdCheckinRepo)
    ioc.register(
        UntappdCheckinScraper, lambda: RequestsUntappdCheckinScraper(untappd_cookie)
    )
    
    # Tinkoff Investments
    ioc.register(
        TinkoffCandlesRepo,
        lambda: TinkoffInvestCandlesRepo(tinkoff_invest_token),
    )
    
    # Users
    ioc.register(CheckTgAdmin, lambda: CheckTgAdmin(tg_admins))

    return ioc
