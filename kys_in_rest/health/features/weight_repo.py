import abc

from kys_in_rest.health.entities.weight import WeightEntry


class WeightRepo:
    @abc.abstractmethod
    def add_weight_entry(self, entry: WeightEntry): ...

    @abc.abstractmethod
    def list_weight_entries(self) -> list[WeightEntry]: ...
