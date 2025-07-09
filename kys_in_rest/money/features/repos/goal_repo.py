import abc
import datetime

from kys_in_rest.money.entities.goal import MoneyGoal


class MoneyGoalRepo(abc.ABC):
    @abc.abstractmethod
    def list_actual(self, now: datetime.date = None) -> list[MoneyGoal]:
        raise NotImplementedError()

    @abc.abstractmethod
    def insert(self, goal: MoneyGoal) -> None:
        raise NotImplementedError()
