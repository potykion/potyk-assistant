from collections import defaultdict

from kys_in_rest.core.str_utils import split_strip
from kys_in_rest.core.tg_utils import escape, TgFeature, AskForData
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.entries.tag import tag_groups
from kys_in_rest.restaurants.features.list_metro import list_metro_items
from kys_in_rest.restaurants.features.ports import RestRepo


class GetNearRestaurants(TgFeature):
    def __init__(self, rest_repo: RestRepo):
        self.rest_repo = rest_repo

    def do(
        self,
        text: str | None,
        tg_user_id: int,
    ) -> str:
        metro = text
        if not metro:
            raise AskForData(
                "Гдэ???",
                options=list_metro_items(),
            )

        metro_rests = self.rest_repo.list_restaurants(metro, rating=7)

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
                    yield f'• [{escape(rest["name"])}]({rest["yandex_maps"]})'
                    if rest.get("comment") or rest.get("from_channel"):
                        comment = escape(rest["comment"])

                        if rest.get("from_channel"):
                            if rest["from_post"]:
                                comment = f'{comment} © [{rest["from_channel"]}]({rest["from_post"]})'
                            else:
                                comment = f'{comment} © {rest["from_channel"]}'
                        yield f"_{comment}_"

                    yield ""

        message = "\n".join(_gen())

        return message
