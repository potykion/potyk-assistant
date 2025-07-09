import sqlite3
from typing import Sequence

from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.infra.beer_post_repo import SqliteBeerPostRepo
from kys_in_rest.core.ioc import IOC
from kys_in_rest.core.sqlite_utils import make_sqlite_cursor
from kys_in_rest.health.features.weight_repo import WeightRepo
from kys_in_rest.health.infra.weight_repo import SqliteWeightRepo
from kys_in_rest.money.features.repos.goal_repo import MoneyGoalRepo
from kys_in_rest.money.features.repos.spending_repo import SpendingRepo
from kys_in_rest.money.infra.goal_repo import SqliteMoneyGoalRepo
from kys_in_rest.money.infra.spending_repo import SqliteSpendingRepo
from kys_in_rest.music.features.download_repo import DownloadRepo
from kys_in_rest.music.infra.download_repo import (
    UrlDownloadRepo,
    YandexMusicDownloadRepo,
)
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.restaurants.infra.rest_repo import SqliteRestRepo
from kys_in_rest.tg.entities.command import TgCommandSetup
from kys_in_rest.tg.features.flow_repo import FlowRepo
from kys_in_rest.tg.infra.flow_repo import SqliteFlowRepo
from kys_in_rest.wishlist.features.wishlist import WishlistRepo
from kys_in_rest.wishlist.infra.wishlist_repo import SqliteWishlistRepo


def make_ioc(
    *,
    db_path: str,
    tg_admins: list[int],
    tg_commands: Sequence[TgCommandSetup] = (),
    yandex_music_token: str,
) -> IOC:
    ioc = IOC()

    # deps
    ioc.register("db_path", db_path)
    ioc.register("tg_admins", tg_admins)
    ioc.register("tg_commands", tg_commands)
    ioc.register(
        sqlite3.Cursor,
        make_sqlite_cursor,
        cache=True,
        teardown=lambda cursor: cursor.connection.close(),
    )

    # repos
    ioc.register(RestRepo, SqliteRestRepo)
    ioc.register(FlowRepo, SqliteFlowRepo)
    ioc.register(BeerPostRepo, SqliteBeerPostRepo)
    ioc.register(WeightRepo, SqliteWeightRepo)
    ioc.register(WishlistRepo, SqliteWishlistRepo)
    ioc.register(SpendingRepo, SqliteSpendingRepo)
    ioc.register(MoneyGoalRepo, SqliteMoneyGoalRepo)
    ioc.register(
        DownloadRepo,
        lambda: UrlDownloadRepo(
            YandexMusicDownloadRepo(yandex_music_token),
        ),
    )

    return ioc
