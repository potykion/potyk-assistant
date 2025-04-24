import abc

from kys_in_rest.tg.entities.flow import TgFlow, TgCommand


class FlowRepo:
    @abc.abstractmethod
    def get_current_flow(self) -> TgFlow: ...

    @abc.abstractmethod
    def start_or_continue_flow(self, command: TgCommand) -> TgFlow: ...
