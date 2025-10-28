import abc
from datetime import datetime

from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin


class UntappdCheckinRepo:
    @abc.abstractmethod
    def insert_checkins(self, checkins: list[UntappdCheckin]) -> None: ...

    @abc.abstractmethod
    def checkin_exists(self, checkin_id: int) -> bool: ...

    @abc.abstractmethod
    def any_checkin_exists(self, checkins: list[UntappdCheckin]) -> set[int]: ...

    @abc.abstractmethod
    def get_checkins_since(self, since: datetime) -> list[UntappdCheckin]: ...
