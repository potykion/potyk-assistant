from collections import defaultdict
from typing import Generator

from kys_in_rest.core.str_utils import split_strip
from kys_in_rest.core.tg_utils import escape, TgFeature, AskForData, TgMsgToSend
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.entries.tag import tag_groups
from kys_in_rest.restaurants.features.list_metro import list_metro_items
from kys_in_rest.restaurants.features.list_tags import list_tag_groups
from kys_in_rest.restaurants.features.ports import RestRepo
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class GetNearRestaurants(TgFeature):
    def __init__(self, rest_repo: RestRepo):
        self.rest_repo = rest_repo

    def do(
        self,
        msg: InputTgMsg,
    ) -> str:
        metro = msg.text
        if not metro:
            raise AskForData(TgMsgToSend("Гдэ???", list_metro_items()))

        metro_rests: list[Restaurant] = self.rest_repo.list_restaurants(
            metro=metro, rating=7
        )

        def _gen():
            yield f"*{metro_colors[metro]} {metro.upper()}*"
            yield ""

            if not metro_rests:
                yield f"Рестораны рядом с метро {metro} не найдены"
                return

            metro_rests_by_tag_groups = defaultdict(list)
            for rest in metro_rests:
                for group, tags in tag_groups.items():
                    if frozenset(split_strip(rest.get("tags") or "")) & frozenset(tags):
                        metro_rests_by_tag_groups[group].append(rest)

            for tag_group, tag_rests in sorted(metro_rests_by_tag_groups.items()):
                yield f"*{tag_group}*"

                for rest in tag_rests:
                    yield from _rest_to_tg_strings(rest)

        message = "\n".join(_gen())
        return message


class FindCategoryRestaurants(TgFeature):
    def __init__(self, rest_repo: RestRepo):
        self.rest_repo = rest_repo

    def do(self, msg: InputTgMsg) -> str:
        tag_group = msg.text
        if not tag_group:
            raise AskForData(TgMsgToSend("Выбери категорию", list_tag_groups()))

        tags = tag_groups[tag_group]

        rests: list[Restaurant] = self.rest_repo.list_restaurants(tags=tags, rating=7)

        def _gen():
            yield f"*{tag_group}*"
            yield ""

            for rest in rests:
                yield from _rest_to_tg_strings(rest, with_metro=True)

        message = "\n".join(_gen())
        return message


def _rest_to_tg_strings(
    rest: Restaurant,
    *,
    with_metro=False,
) -> Generator[str, None, None]:
    rest_line = f'• [{escape(rest["name"])}]({rest["yandex_maps"]})'
    if with_metro:
        rest_line = f"{rest_line} @ {rest['metro']}"
    yield rest_line
    if rest.get("comment") or rest.get("from_channel"):
        comment = escape(rest["comment"])

        if rest.get("from_channel"):
            if rest["from_post"]:
                comment = f'{comment} © [{rest["from_channel"]}]({rest["from_post"]})'
            else:
                comment = f'{comment} © {rest["from_channel"]}'
        yield f"_{comment}_"
    yield ""
