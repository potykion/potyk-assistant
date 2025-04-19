import json
import os

metro_colors = {
    "Калужская": "🟠",
    "Киевская": "🔵",
    "Китай Город": "🟠",
    "Кузнецкий мост": "🟣",
    "Лубянка": "🔴",
    "Новослободская": "🩶",
    "Пушкинская": "🟣",
    "Раменки": "🟡",
    "Смоленская": "🔵",
    "Сухаревская": "🟠",
    "Трубная": "🩶",
    "Улица 1905 года": "🟣",
    "Университет": "🔴",
    "Цветной бульвар": "🩶",
    "Чистые пруды": "🔴",
}
tag_names = {
    "ramen": "РАМЕН",
    "tom-yam": "ТОМ ЯМ",
    "chinese": "КИТАЙКИ",
    "korean": "КОРЕЙКИ",
    "kebab": "КЕБАБЫ ДЮРУМЫ",
    "shawarma": "ШАУРМА",
    "burger": "БУРГЕРЫ",
    "sandwich": "СЭНДВИЧИ",
    "italian": "ИТАЛИЯ",
    "spanish": "ИСПАНИЯ",
    "fish": "РЫБА",
}


def load_rests():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "rests.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def near(metro: str):
    rests = load_rests()

    def _gen():
        metro_rests = [rest for rest in rests if rest["metro"].lower() == metro.lower()]

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
                    comment = rest["comment"]

                    if rest.get("from_channel"):
                        if rest["from_post"]:
                            comment = f'{comment} © [{rest["from_channel"]}]({rest["from_post"]})'
                        else:
                            comment = f'{comment} © {rest["from_channel"]}'
                    yield f'_{comment}_'

                yield ""

    return "\n".join(_gen()).replace(".", r"\.")
