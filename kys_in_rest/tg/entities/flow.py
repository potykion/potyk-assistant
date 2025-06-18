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


class TgFlow(NamedTuple):
    command: TgCommand
    tg_user_id: int
