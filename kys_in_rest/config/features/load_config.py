from kys_in_rest.config.entities.config import Config
from kys_in_rest.config.features.repos.config_repo import ConfigRepo


class LoadConfig:
    def __init__(self, config_repo: ConfigRepo):
        self.config_repo = config_repo

    def do(self) -> Config:
        return self.config_repo.load()