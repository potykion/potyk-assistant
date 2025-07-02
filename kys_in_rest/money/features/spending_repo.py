import abc

from kys_in_rest.money.entities.spending import Spending


class SpendingRepo(abc.ABC):
    @abc.abstractmethod
    def add_spending(self, spending: Spending):
        raise NotImplementedError()
