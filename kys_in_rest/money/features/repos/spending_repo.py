import abc
from datetime import datetime

from kys_in_rest.money.entities.spending import Spending


class SpendingRepo(abc.ABC):
    @abc.abstractmethod
    def add_spending(self, spending: Spending) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def list_today(self, now: datetime | None = None) -> list[Spending]:
        raise NotImplementedError()
