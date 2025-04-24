import enum
from typing import NamedTuple


class TgCommand(enum.StrEnum):
    near = enum.auto()
    new = enum.auto()


class TgFlow(NamedTuple):
    command: TgCommand
    tg_user_id: int
