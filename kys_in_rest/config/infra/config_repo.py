import json

from kys_in_rest.config.entities.config import Config
from kys_in_rest.config.features.repos.config_repo import ConfigRepo
from kys_in_rest.core.sqlite_utils import SqliteRepo


class SqliteConfigRepo(SqliteRepo, ConfigRepo):
    def load(self) -> Config:
        row = self.cursor.execute("select * from config").fetchone()
        if not row:
            config = Config()
            config_json = config.model_dump(mode="json")
            self.cursor.execute(
                "insert into config (config_json) values (?)",
                (json.dumps(config_json),),
            )
            self.cursor.connection.commit()
            return config

        return Config(**row["config_json"])

    def save(self, config: Config) -> None:
        config_json = config.model_dump(mode="json")
        self.cursor.execute("update config set config_json=?", (config_json,))
        self.cursor.connection.commit()
