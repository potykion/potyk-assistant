import abc

from kys_in_rest.core.sqlite_utils import SqliteRepo
from kys_in_rest.tg.entities.my_tg_channel import MyTgChannel
from kys_in_rest.tg.features.repos.my_tg_channels_repo import MyTgChannelsRepo


class SqliteMyTgChannelsRepo(SqliteRepo, MyTgChannelsRepo):
    def list(self) -> list[MyTgChannel]:
        rows = self.cursor.execute("select * from my_tg_channels")
        return [MyTgChannel(**row) for row in rows]
