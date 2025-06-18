import abc
from typing import Any

from kys_in_rest.core.tg_utils import TgFeature
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg
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
    ):
        self.check_tg_admin = check_tg_admin
        self.wishlist_repo = wishlist_repo

    def do(self, msg: InputTgMsg) -> str | tuple[str, dict[str, Any]]:
        self.check_tg_admin.do(msg.tg_user_id)

        if msg.text:
            self.wishlist_repo.add(msg.text)
            return "Записал 👌"

        wishlist_items = self.wishlist_repo.list_not_received()
        wishlist_items_str = "\n".join(f"• {wi.name}" for wi in wishlist_items)
        return f"Вишлист:\n{wishlist_items_str}"
