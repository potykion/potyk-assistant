from typing import NamedTuple, Callable

from kys_in_rest.core.str_utils import parse_link
from kys_in_rest.core.tg_utils import AskForData, TgCbOption
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.features.list_metro import list_metro_items
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
]


class AddNewRestaurant:
    def __init__(self, rest_repo: RestRepo) -> None:
        self.rest_repo = rest_repo

    def do(self, text: str = None):
        rest, _ = self.rest_repo.get_or_create_draft()
        rest: Restaurant

        for param in rest_params:
            if not rest.get(param.name):
                if param.parser and text:
                    text = param.parser(text)

                if not text:
                    raise AskForData(
                        param.question,
                        param.name,
                        param.options() if param.options else None,
                    )

                rest[param.name] = text
                self.rest_repo.update_draft(rest)
                text = None

        rest["draft"] = False
        self.rest_repo.update_draft(rest)

        return rest
