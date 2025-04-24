import sqlite3

from kys_in_rest.tg.entities.flow import TgFlow
from kys_in_rest.tg.features.flow_repo import FlowRepo


class SqliteFlowRepo(FlowRepo):

    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def get_flow(self) -> TgFlow:
        pass
