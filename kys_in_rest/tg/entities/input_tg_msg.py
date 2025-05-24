from typing import NamedTuple, cast, Self, Any
from telegram import Update, CallbackQuery, Message, MessageOrigin, User

channels = [
    (-1001074974864, "4BREWERS", "https://t.me/fourbrewers"),
]


class InputTgMsg(NamedTuple):
    text: str | None
    tg_user_id: int
    forward_link: str | None = None
    forward_channel_name: str | None = None
    forward_channel_id: str | None = None

    @classmethod
    def parse(
        cls,
        update_or_query: Update | CallbackQuery,
    ) -> Self:
        if isinstance(update_or_query, CallbackQuery):
            text = update_or_query.data
            user = update_or_query.from_user
            return cls(text=text, tg_user_id=user.id)

        message = cast(Message, update_or_query.message)
        text = message.text or message.caption

        forward_link = None
        forward_channel_name = None
        forward_channel_id = None
        if origin := message.forward_origin:
            if hasattr(origin, "chat") and hasattr(origin.chat, "link") and hasattr(origin.chat, "effective_name") and hasattr(origin.chat, "id"):
                forward_link = f"{origin.chat.link}/{cast(Any, origin).message_id}"
                forward_channel_name = origin.chat.effective_name
                forward_channel_id = str(origin.chat.id)

        user = cast(User, update_or_query.effective_user)
        return cls(
            text=text,
            tg_user_id=user.id,
            forward_link=forward_link,
            forward_channel_name=forward_channel_name,
            forward_channel_id=forward_channel_id,
        )
