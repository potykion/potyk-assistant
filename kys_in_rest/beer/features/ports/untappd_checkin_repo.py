import abc


class UntappdCheckinRepo:
    @abc.abstractmethod
    def insert_checkins(self, checkins: list) -> None:
        ...

    @abc.abstractmethod
    def checkin_exists(self, checkin_id: int) -> bool:
        ...
