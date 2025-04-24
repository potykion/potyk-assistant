import itertools
from typing import NamedTuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def escape(text):
    to_escape = ".()-!+"
    for ch in to_escape:
        text = text.replace(ch, rf"\{ch}")
    return text


class TgCbOption(NamedTuple):
    label: str
    cb_data: str


class AskForData(Exception):
    def __init__(
        self,
        question: str,
        field: str | None = None,
        options: list[TgCbOption] = None,
    ):
        self.question = question
        self.field = field
        self.options = options


def build_keyboard(options: list[TgCbOption], buttons=3):
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
    def do(self, text: str | None = None) -> str: ...
