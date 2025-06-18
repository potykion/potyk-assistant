import enum
from typing import NamedTuple


class TgCommand(enum.StrEnum):
    near = enum.auto()
    category = enum.auto()
    new = enum.auto()
    new_beer = enum.auto()
    weight = enum.auto()
    id = enum.auto()


class TgFlow(NamedTuple):
    command: TgCommand
    tg_user_id: int
