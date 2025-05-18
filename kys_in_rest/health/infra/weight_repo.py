from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo


class SqliteWeightRepo(WeightRepo, SqliteRepo):

    def add_weight_entry(self, entry: WeightEntry):
        self.cursor.execute(
            "insert into weight (date, weight) values (?, ?)",
            (entry.date, entry.weight),
        )

    def list_weight_entries(self) -> list[WeightEntry]:
        pass
