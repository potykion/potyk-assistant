import abc
import datetime

from kys_in_rest.core.zen_money import ZenMoneyDiffRaw
from kys_in_rest.money.entities.zen_money import ZenMoneyDiff


class ZenMoneyRepo(abc.ABC):
    @abc.abstractmethod
    def sync(self, current_client_timestamp: int | None = None, server_timestamp: int = 0) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, diff: ZenMoneyDiffRaw) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_current(self) -> ZenMoneyDiff | None:
        raise NotImplementedError

    @abc.abstractmethod
    def monthly_spent(self, current_date: datetime.date = None) -> ZenMoneyDiffRaw:
        raise NotImplementedError
