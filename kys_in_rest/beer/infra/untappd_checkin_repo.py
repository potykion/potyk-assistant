from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.core.sqlite_utils import SqliteRepo


class SqliteUntappdCheckinRepo(SqliteRepo, UntappdCheckinRepo):
    def insert_checkins(self, checkins: list[UntappdCheckin]) -> None:
        self.cursor.executemany(
            """
                INSERT INTO untappd_checkins (
                    id,
                    beer_url,
                    beer_img,
                    beer_name,
                    beer_brewery,
                    beer_brewery_url,
                    checkin_location,
                    checkin_location_url,
                    checkin_comment,
                    checkin_rating,
                    checkin_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            [
                (
                    checkin.id,
                    checkin.beer_url,
                    checkin.beer_img,
                    checkin.beer_name,
                    checkin.beer_brewery,
                    checkin.beer_brewery_url,
                    checkin.checkin_location,
                    checkin.checkin_location_url,
                    checkin.checkin_comment,
                    checkin.checkin_rating,
                    checkin.checkin_date,
                )
                for checkin in checkins
            ],
        )
        self.cursor.connection.commit()

    def checkin_exists(self, checkin_id: int) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM untappd_checkins WHERE id = ? LIMIT 1",
            (checkin_id,),
        )
        return self.cursor.fetchone() is not None
