from datetime import datetime

from kys_in_rest.beer.entities.untappd_checkin import UntappdCheckin
from kys_in_rest.beer.features.ports.untappd_checkin_repo import UntappdCheckinRepo
from kys_in_rest.core.sqlite_utils import SqliteRepo


class SqliteUntappdCheckinRepo(SqliteRepo, UntappdCheckinRepo):
    def any_checkin_exists(self, checkins: list[UntappdCheckin]) -> set[int]:
        rows = self.cursor.execute(
            "select id from untappd_checkins where id in ({})".format(
                ",".join("?" for _ in checkins)
            ),
            tuple(checkin.id for checkin in checkins),
        ).fetchall()
        return {row["id"] for row in rows}

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

    def get_checkins_since(self, since: datetime) -> list[UntappdCheckin]:
        since_str = since.strftime("%a, %d %b %Y %H:%M:%S %z")
        rows = self.cursor.execute(
            "SELECT * FROM untappd_checkins WHERE checkin_date >= ? ORDER BY checkin_date DESC",
            (since_str,),
        ).fetchall()
        
        return [
            UntappdCheckin(
                id=row["id"],
                beer_url=row["beer_url"],
                beer_img=row["beer_img"],
                beer_name=row["beer_name"],
                beer_brewery=row["beer_brewery"],
                beer_brewery_url=row["beer_brewery_url"],
                checkin_location=row["checkin_location"],
                checkin_location_url=row["checkin_location_url"],
                checkin_comment=row["checkin_comment"],
                checkin_rating=row["checkin_rating"],
                checkin_date=row["checkin_date"],
            )
            for row in rows
        ]
