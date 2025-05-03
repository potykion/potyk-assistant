from typing_extensions import NamedTuple

from kys_in_rest.beer.entities.beer_post import hops, fruits, BeerStyleName, BeerStyle


class StyleParser(NamedTuple):
    parsed_style: str
    pattern: str
    parse_hops: bool = False
    parse_fruits: bool = False
    # Кейс слово Эль + есть фрукты в тексте
    match_if_parsed_fruits: bool = False


style_parsers = [
    StyleParser(BeerStyleName.WEIZEN, "Weizen"),
    StyleParser(BeerStyleName.MILK_STOUT, "Молочный стаут"),
    StyleParser(BeerStyleName.TIPA, "тройной индийский пэйл эль", parse_hops=True),
    StyleParser(BeerStyleName.NE_IPA, "новоанглийских индиа пейл элей", parse_hops=True),
    StyleParser(BeerStyleName.NE_IPA, "NE IPA", parse_hops=True),
    StyleParser(BeerStyleName.IPA, "American IPA", parse_hops=True),
    StyleParser(BeerStyleName.MEAD, "мид", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "саур эль", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "кислый эль", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "Sour", parse_fruits=True),
    StyleParser(
        BeerStyleName.SOUR_ALE, "эль", parse_fruits=True, match_if_parsed_fruits=True
    ),
]


def parse_name(text: str) -> str: ...


def parse_style(text: str) -> BeerStyle:
    lower = text.lower()

    style = ""
    style_hops = []
    style_fruits = []

    for parser in style_parsers:
        # Проверка наличия паттерна
        if parser.pattern.lower() in lower:
            # Кейс слово Эль + есть фрукты в тексте
            if parser.match_if_parsed_fruits:
                if not (style_fruits := _parse_fruits(lower)):
                    continue

            style = parser.parsed_style
            if parser.parse_hops:
                style_hops = _parse_hops(lower)
            if parser.parse_fruits:
                style_fruits = _parse_fruits(lower)

            break

    return BeerStyle(
        name=style,
        hops=style_hops,
        fruits=style_fruits,
    )


def _parse_hops(lower):
    style_hops = []
    for hop in hops:
        if hop.lower() in lower:
            style_hops.append(hop)
    return style_hops


def _parse_fruits(text):
    style_fruits = []
    for fruit_case, fruit in fruits:
        if fruit_case.lower() in text.lower():
            style_fruits.append(fruit)
    return style_fruits
