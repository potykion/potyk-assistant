from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.health.entities.weight import WeightEntry
from kys_in_rest.health.features.weight_repo import WeightRepo


class SqliteWeightRepo(WeightRepo, SqliteRepo):
    def add_weight_entry(self, entry: WeightEntry) -> None:
        self.cursor.execute(
            "insert into weight (date, weight) values (?, ?)",
            (entry.date, entry.weight),
        )
        self.cursor.connection.commit()

    def list_weight_entries(self) -> list[WeightEntry]:
        rows = self.cursor.execute("select * from weight order by date").fetchall()
        return [WeightEntry(**row) for row in rows]

    def get_last(self) -> WeightEntry | None:
        row = self.cursor.execute(
            "select * from weight order by date desc limit 1"
        ).fetchone()
        if not row:
            return None
        return WeightEntry(**row)
