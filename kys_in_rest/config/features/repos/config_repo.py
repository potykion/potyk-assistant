import abc

from kys_in_rest.config.entities.config import Config


class ConfigRepo(abc.ABC):
    @abc.abstractmethod
    def load(self) -> Config:
        raise NotImplementedError()