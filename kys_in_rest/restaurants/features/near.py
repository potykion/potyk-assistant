from kys_in_rest.core.tg_utils import escape
from kys_in_rest.restaurants.entries.metro import metro_colors
from kys_in_rest.restaurants.entries.tag import tag_names
from kys_in_rest.restaurants.infra.rest_repo import load_rests


def near(metro: str):
    metro_rests = load_rests(metro)

    def _gen():
        if not metro_rests:
            yield f"Рестораны рядом с метро {metro} не найдены"
            return

        yield f'*{metro_colors[metro_rests[0]["metro"]]} {metro_rests[0]["metro"].upper()}*'
        yield ""

        metro_rests_by_tags = {}
        for rest in metro_rests:
            if not rest["tags"]:
                continue

            primary_tag = tuple(sorted(rest["tags"]))
            if primary_tag not in metro_rests_by_tags:
                metro_rests_by_tags[primary_tag] = []
            metro_rests_by_tags[primary_tag].append(rest)

        for tags, tag_rests in sorted(metro_rests_by_tags.items()):
            yield " ".join(f"*{tag_names[tag]}*" for tag in tags)

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
