import sqlite3

from kys_in_rest.tg.entities.flow import TgFlow
from kys_in_rest.tg.features.flow_repo import FlowRepo


class SqliteFlowRepo(FlowRepo):

    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def get_current_flow(self, tg_user_id) -> TgFlow:
        row = self.cursor.execute(
            "select * from flow where tg_user_id = ?",
            (tg_user_id,),
        ).fetchone()
        if not row:
            raise Exception(f"No current flow for {tg_user_id=}")
        return TgFlow(**row)

    def start_or_continue_flow(
        self,
        command,
        tg_user_id: int,
    ) -> TgFlow:
        row = self.cursor.execute(
            "select * from flow where command = ? and tg_user_id = ?",
            (command, tg_user_id),
        ).fetchone()
        if not row:
            self.cursor.execute(
                "delete from flow where tg_user_id = ?",
                (tg_user_id,),
            )
            self.cursor.execute(
                """insert into flow (command, tg_user_id) values (?, ?);""",
                (command, tg_user_id),
            )
            self.cursor.connection.commit()
            return TgFlow(command=command, tg_user_id=tg_user_id)
        else:
            return TgFlow(**row)
