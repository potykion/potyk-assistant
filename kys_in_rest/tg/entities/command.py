import dataclasses
from typing import Type

from kys_in_rest.core.tg_utils import (
    TgFeature,
)
from kys_in_rest.tg.entities.flow import TgCommand


@dataclasses.dataclass
class TgCommandSetup:
    command: TgCommand
    desc: str
    feature: Type[TgFeature]
