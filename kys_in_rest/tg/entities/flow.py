import enum
from typing import NamedTuple


class TgCommand(enum.StrEnum):
    rest_cat = enum.auto()
    rest_metro = enum.auto()
    new = enum.auto()
    new_beer = enum.auto()
    weight = enum.auto()
    id = enum.auto()
    help = enum.auto()
    start = enum.auto()
    wishlist = enum.auto()
    wishlist_ru = "вишлист"
    w = enum.auto()
    weight_ru = "вес"
    download = enum.auto()
    mu = enum.auto()
    spend = enum.auto()
    mon_goal_budget = enum.auto()
    mon_goal = enum.auto()
    mon = enum.auto()
    spend_ru = "траты"
    zen_money_sync = enum.auto()
    my_tg_channels = enum.auto()


class TgFlow(NamedTuple):
    command: TgCommand
    tg_user_id: int
