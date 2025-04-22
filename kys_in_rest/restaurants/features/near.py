from collections import defaultdict

from kys_in_rest.core.tg_utils import escape
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.entries.tag import tag_groups
from kys_in_rest.restaurants.infra.rest_repo import load_rests


def near(metro: str):
    metro_rests = load_rests(metro)

    def _gen():
        yield f'*{metro_colors[metro]} {metro.upper()}*'
        yield ""

        if not metro_rests:
            yield f"Рестораны рядом с метро {metro} не найдены"
            return


        metro_rests_by_tag_groups = defaultdict(list)
        for rest in metro_rests:
            for group, tags in tag_groups.items():
                if frozenset(rest["tags"].split(",")) & frozenset(tags):
                    metro_rests_by_tag_groups[group].append(rest)

        for tag_group, tag_rests in sorted(metro_rests_by_tag_groups.items()):
            yield f"*{tag_group}*"

            for rest in tag_rests:
                yield f'• [{rest["name"]}]({rest["yandex_maps"]})'
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
