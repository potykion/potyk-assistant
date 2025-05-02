import json
import sqlite3

from kys_in_rest.beer.entities.beer_post import BeerPost
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo


class SqliteBeerPostRepo(BeerPostRepo):
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def start_new_post(self):
        post = BeerPost.new()
        self.cursor.execute(
            """
        insert into beer_posts (created, beers) VALUES  (?, ?)
        """,
            (
                post.created.strftime("%Y-%m-%d %H:%M:%S"),
                json.dumps(post.beers),
            ),
        )
        self.cursor.connection.commit()

    def get_last_post(self) -> BeerPost:
        row = self.cursor.execute(
            "select * from beer_posts order by created desc limit 1"
        ).fetchone()
        return BeerPost(
            id=row["id"],
            created=row["created"],
            beers=json.loads(row["beers"]),
        )

    def update_post(self, post) -> None:
        post_json = post.model_dump(mode="json")
        self.cursor.execute(
            """
            update beer_posts set beers = ? where id = ?""",
            (
                json.dumps(post_json["beers"]),
                post.id,
            ),
        )
        self.cursor.connection.commit()
