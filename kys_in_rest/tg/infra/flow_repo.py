import sqlite3

from kys_in_rest.tg.entities.flow import TgFlow
from kys_in_rest.tg.features.flow_repo import FlowRepo


class SqliteFlowRepo(FlowRepo):

    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def get_current_flow(self) -> TgFlow:
        row = self.cursor.execute("select * from flow").fetchone()
        if not row:
            raise Exception("No current flow")
        return TgFlow(**row)

    def start_or_continue_flow(self, command) -> TgFlow:
        row = self.cursor.execute(
            "select * from flow where command = ?", (command,)
        ).fetchone()
        if not row:
            self.cursor.execute("delete from flow;")
            self.cursor.execute(
                """insert into flow (command) values (?);""", (command,)
            )
            self.cursor.connection.commit()
            return TgFlow(command=command)
        else:
            return TgFlow(**row)
