import os

from kys_in_rest.core.tg_utils import SendTgMessageInterrupt, TgMsgToSend


class CheckTgAdmin:
    """
    Проверяет, может ли Телеграм юзер выполнять действие (является ли он админом)

    Пример:
    >>> class Feature(TgFeature):
    ... def __init__(
    ...     self,
    ...     check_tg_admin: CheckTgAdmin,
    ... ) -> None:
    ...     self.check_tg_admin = check_tg_admin
    ...
    ... def do(self, msg: InputTgMsg) -> str:
    ...     self.check_tg_admin.do(msg.tg_user_id) # doctest: +SKIP
    """
    def __init__(self, tg_admins: list[int]):
        self.tg_admins = tg_admins

    def do(self, tg_user_id):
        if int(tg_user_id) not in self.tg_admins:
            raise SendTgMessageInterrupt(TgMsgToSend("Тебе нельзя"))
