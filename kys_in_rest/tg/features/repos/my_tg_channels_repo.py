import abc

from kys_in_rest.tg.entities.my_tg_channel import MyTgChannel


class MyTgChannelsRepo(abc.ABC):
    @abc.abstractmethod
    def list(self) -> list[MyTgChannel]:
        raise NotImplementedError()
