import abc
from typing import Any

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.users.features.check_admin import CheckTgAdmin
from kys_in_rest.wishlist.entities.wishlist_item import WishlistItem


class WishlistRepo(abc.ABC):
    @abc.abstractmethod
    def list_not_received(self) -> list[WishlistItem]: ...

    @abc.abstractmethod
    def add(self, name: str) -> WishlistItem: ...


class Wishlist(TgFeature):
    def __init__(
        self,
        check_tg_admin: CheckTgAdmin,
        wishlist_repo: WishlistRepo,
        bot_msg_repo: BotMsgRepo,
    ):
        self.check_tg_admin = check_tg_admin
        self.wishlist_repo = wishlist_repo
        self.bot_msg_repo = bot_msg_repo

    async def do_async(self, msg: InputTgMsg) -> None:
        self.check_tg_admin.do(msg.tg_user_id)

        if msg.text:
            self.wishlist_repo.add(msg.text)
            await self.bot_msg_repo.send_text("Записал 👌")
            return

        # Показываем справку если нет аргументов
        await self.bot_msg_repo.send_text(
            "Чтобы добавить пиши <code>/wishlist предмет</code>"
        )

        wishlist_items = self.wishlist_repo.list_not_received()
        if wishlist_items:
            wishlist_items_str = "\n".join(f"• {wi.name}" for wi in wishlist_items)
            wishlist_items_str = "<b>Вишлист:</b>\n" + wishlist_items_str

            await self.bot_msg_repo.send_text(wishlist_items_str)
        else:
            await self.bot_msg_repo.send_text("Вишлист пуст")
