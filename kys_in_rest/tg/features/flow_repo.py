import abc

from kys_in_rest.tg.entities.flow import TgFlow


class FlowRepo:
    @abc.abstractmethod
    def get_flow(self) -> TgFlow:
        ...
