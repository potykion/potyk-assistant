from typing import NamedTuple

from telegram import Update, CallbackQuery

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
    ):

        if isinstance(update_or_query, CallbackQuery):
            text = update_or_query.data
            return cls(text=text, tg_user_id=update_or_query.from_user.id)

        text = update_or_query.message.text or update_or_query.message.caption

        forward_link = None
        forward_channel_name = None
        forward_channel_id = None
        if origin := update_or_query.message.forward_origin:
            forward_link = f"{origin.chat.link}/{origin.message_id}"
            forward_channel_name = origin.chat.effective_name
            forward_channel_id = origin.chat.id

        return cls(
            text=text,
            tg_user_id=update_or_query.effective_user.id,
            forward_link=forward_link,
            forward_channel_name=forward_channel_name,
            forward_channel_id=forward_channel_id,
        )
