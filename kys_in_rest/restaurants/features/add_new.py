import os
from typing import NamedTuple, Callable

from kys_in_rest.core.str_utils import parse_link
from kys_in_rest.core.tg_utils import (
    AskForData,
    TgCbOption,
    TgFeature,
    SendTgMessageInterrupt,
    TgMsgToSend,
)
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.features.list_metro import list_metro_items
from kys_in_rest.restaurants.features.list_tags import list_tag_items
from kys_in_rest.restaurants.features.ports import RestRepo


class RestParam(NamedTuple):
    name: str
    question: str
    parser: Callable[[str], str | None] | None = None
    options: Callable[[], list[TgCbOption]] | None = None


rest_params = [
    RestParam("name", "Как называется?"),
    RestParam("yandex_maps", "Скинь ссылку на Яндекс Карты", parse_link),
    RestParam("metro", "Какое метро?", options=lambda: list_metro_items()),
    RestParam("tags", "Какая кухня?", options=lambda: list_tag_items()),
    RestParam("from_", 'Откуда узнал? Пришли репост или пришли "-"'),
    RestParam("comment", "Комментарии будут? Типа что брать?"),
]


class AddNewRestaurant(TgFeature):
    def __init__(self, rest_repo: RestRepo) -> None:
        self.rest_repo = rest_repo

    def do(self, msg):
        if int(msg.tg_user_id) != int(os.environ["TG_ADMIN"]):
            raise SendTgMessageInterrupt(TgMsgToSend("Тебе нельзя"))

        text = msg.text

        rest, _ = self.rest_repo.get_or_create_draft()
        rest: Restaurant

        for param in rest_params:
            if param.name == "from_":
                if rest["from_channel"] and rest["from_post"]:
                    continue

                if not text:
                    raise AskForData(
                        TgMsgToSend(
                            param.question,
                            param.options() if param.options else None,
                        )
                    )

                if text == "-":
                    rest["from_channel"] = text
                    rest["from_post"] = text
                    self.rest_repo.update_draft(rest)
                    text = None
                elif msg.forward_link:
                    rest["from_channel"] = msg.forward_channel_name
                    rest["from_post"] = msg.forward_link
                    self.rest_repo.update_draft(rest)
                    text = None

            else:
                if not rest.get(param.name):
                    if param.parser and text:
                        text = param.parser(text)

                    if not text:
                        raise AskForData(
                            TgMsgToSend(
                                param.question,
                                param.options() if param.options else None,
                            )
                        )

                    if param.name == "name":
                        if not self.rest_repo.check_name_unique(text):
                            raise AskForData(
                                TgMsgToSend("Такой рестик уже был, введи другой")
                            )

                    rest[param.name] = text
                    self.rest_repo.update_draft(rest)
                    text = None

        rest["draft"] = False
        self.rest_repo.update_draft(rest)
        return "Записал 👌"
