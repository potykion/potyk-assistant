from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.core.sqlite_utils import SqliteRepo


class SqliteUntappdCheckinRepo(SqliteRepo, UntappdCheckinRepo):
    def insert_checkins(self, checkins: list) -> None:
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
                    checkin.beer_image_url,
                    checkin.beer_name,
                    checkin.brewery_name,
                    checkin.brewery_url,
                    checkin.brewery_location,
                    checkin.brewery_location_url,
                    checkin.checkin_comment,
                    checkin.rating_score,
                    checkin.checkin_time,
                )
                for checkin in checkins
            ],
        )

    def checkin_exists(self, checkin_id: int) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM untappd_checkins WHERE id = ? LIMIT 1",
            (checkin_id,),
        )
        return self.cursor.fetchone() is not None
