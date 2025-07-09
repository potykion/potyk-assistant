import abc
import itertools
from typing import NamedTuple, Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


def tg_escape(text: str) -> str:
    to_escape = ".()-!+|{}"
    for ch in to_escape:
        text = text.replace(ch, rf"\{ch}")
    return text


class TgCbOption(NamedTuple):
    label: str
    cb_data: str


class TgMsgToSend(NamedTuple):
    message: str
    options: list[TgCbOption] | None = None


class SendTgMessageInterrupt(Exception):
    def __init__(self, *messages: TgMsgToSend):
        self.messages = messages


class AskForData(SendTgMessageInterrupt): ...


def build_keyboard(options: list[TgCbOption], buttons: int = 2) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(metro_str, callback_data=metro_cb)
            for (metro_str, metro_cb) in row
        ]
        for row in itertools.batched(options, buttons)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


class TgFeature:
    @abc.abstractmethod
    def do(self, msg: InputTgMsg) -> str | tuple[str, dict[str, Any]]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def do_async(self, msg: InputTgMsg) -> None:
        raise NotImplementedError()
