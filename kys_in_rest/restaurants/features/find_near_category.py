from collections import defaultdict
from typing import Generator, Sequence

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

        def _gen() -> Generator[str, None, None]:
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
                    yield _rest_to_tg_string(rest)

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

        rests: list[Restaurant] = self.rest_repo.list_restaurants(tags=list(tags), rating=7)

        def _gen() -> Generator[str, None, None]:
            yield f"*{tag_group}*"
            yield ""

            for rest in rests:
                yield _rest_to_tg_string(rest, with_metro=True)

        message = "\n".join(_gen())
        return message


def _rest_to_tg_string(
    rest: Restaurant,
    *,
    with_metro: bool = False,
) -> str:
    """
    >>> _rest_to_tg_string(Restaurant(name='Muu', yandex_maps='https://yandex.ru/maps/org/steyk_khaus_muu/132781764150?si=potyk-io', tags=['Американская 🍖'], comment='-', from_channel='-', from_post='-')).strip()
    '• [Muu](https://yandex.ru/maps/org/steyk_khaus_muu/132781764150?si=potyk-io)'
    """

    parts = []

    rest_line = f'• [{escape(str(rest["name"]))}]({rest["yandex_maps"]})'
    if with_metro:
        metro = escape(rest['metro'])
        rest_line = f"{rest_line} @ {metro}"
    parts.append(rest_line)

    if (rest.get("comment") and rest.get("comment") != "-") or (
        rest.get("from_channel") and rest.get("from_channel") != "-"
    ):
        comment_parts = []

        if rest.get("comment") and rest.get("comment") != "-":
            comment_parts.append(escape(str(rest["comment"])))

        if rest.get("from_channel") and rest.get("from_channel") != "-":
            if rest["from_post"]:
                comment_parts.append(f'[{rest["from_channel"]}]({rest["from_post"]})')
            else:
                comment_parts.append(rest["from_channel"])

        comment = " © ".join(comment_parts)

        comment = f"_{comment}_"
        parts.append(comment)

    parts.append("")

    return "\n".join(parts)
