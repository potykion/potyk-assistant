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
    def list_received(self) -> list[WishlistItem]: ...

    @abc.abstractmethod
    def add(self, name: str) -> WishlistItem: ...

    @abc.abstractmethod
    def mark_as_received(self, name: str) -> WishlistItem | None: ...


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
            # Проверяем, не является ли это командой удаления
            if msg.text.startswith('-'):
                item_name = msg.text[1:].strip()
                if item_name:
                    item = self.wishlist_repo.mark_as_received(item_name)
                    if item:
                        await self.bot_msg_repo.send_text(f"✅ Отметил как полученное: {item.name}")
                    else:
                        await self.bot_msg_repo.send_text(f"❌ Предмет '{item_name}' не найден в вишлисте")

                    await self._show_active_wishlist()
                    await self._show_received()
                    return

            # Добавляем новый предмет
            # Сначала проверяем, есть ли предмет в полученных (поиск по началу названия)
            received_items = self.wishlist_repo.list_received()
            was_in_received = any(wi.name.lower().startswith(msg.text.lower()) for wi in received_items)

            item = self.wishlist_repo.add(msg.text)

            if was_in_received:
                await self.bot_msg_repo.send_text(f"🔄 Восстановил из полученных: {item.name}")
            else:
                await self.bot_msg_repo.send_text("Записал 👌")

            await self._show_active_wishlist()
            return

        # Показываем справку и текущий вишлист
        await self.bot_msg_repo.send_text(
            "<i>Чтобы добавить пиши <code>/wishlist предмет</code>\n</i>"
            "<i>Чтобы отметить как полученное пиши <code>/wishlist -предмет</code></i>"
        )

        await self._show_active_wishlist()
        await self._show_received()

    async def _show_received(self):
        received_items = self.wishlist_repo.list_received()
        if received_items:
            received_items_str = "\n".join(f"✅ {wi.name}" for wi in received_items)
            received_items_str = "<b>Полученные:</b>\n" + received_items_str
            await self.bot_msg_repo.send_text(received_items_str)

    async def _show_active_wishlist(self):
        # Показываем активный вишлист
        wishlist_items = self.wishlist_repo.list_not_received()
        if wishlist_items:
            wishlist_items_str = "\n".join(f"• {wi.name}" for wi in wishlist_items)
            wishlist_items_str = "<b>Вишлист:</b>\n" + wishlist_items_str
            await self.bot_msg_repo.send_text(wishlist_items_str)
        else:
            await self.bot_msg_repo.send_text("Активный вишлист пуст")
