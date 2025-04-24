import abc

from kys_in_rest.tg.entities.flow import TgFlow, TgCommand


class FlowRepo:
    @abc.abstractmethod
    def get_current_flow(self, tg_user_id: int) -> TgFlow: ...

    @abc.abstractmethod
    def start_or_continue_flow(
        self,
        command: TgCommand,
        tg_user_id: int,
    ) -> TgFlow: ...
