from nltk import SnowballStemmer, word_tokenize
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
    StyleParser(BeerStyleName.WEIZEN, "weizen"),
    StyleParser(BeerStyleName.NON_ALCO_LAGER, "Non-Alco Lager"),
    StyleParser(BeerStyleName.HELLES, "хеллес"),
    StyleParser(BeerStyleName.LAGER, "lager"),
    StyleParser(BeerStyleName.LAGER, "лагер"),
    StyleParser(BeerStyleName.MILK_STOUT, "молочн стаут"),
    StyleParser(BeerStyleName.TIPA, "тройн индийск пэйл эл", parse_hops=True),
    StyleParser(BeerStyleName.DIPA, "Double IPA", parse_hops=True),
    StyleParser(BeerStyleName.NE_IPA, "новоанглийск инд пейл эл", parse_hops=True),
    StyleParser(BeerStyleName.NE_IPA, "ne ipa", parse_hops=True),
    StyleParser(BeerStyleName.IPA, "american ipa", parse_hops=True),
    StyleParser(BeerStyleName.MEAD, "мид", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "саур", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "саур эл", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "саур-эл", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "кисл эл", parse_fruits=True),
    StyleParser(BeerStyleName.SOUR_ALE, "Sour", parse_fruits=True),
    StyleParser(BeerStyleName.BERLINER, "берлинер", parse_fruits=True),
    StyleParser(
        BeerStyleName.SOUR_ALE, "эл", parse_fruits=True, match_if_parsed_fruits=True
    ),
]


def parse_name(text: str) -> str: ...


def parse_style(text: str) -> BeerStyle | None:
    text = _stem_text(text)

    style = ""
    style_hops = []
    style_fruits = []

    for parser in style_parsers:
        # Проверка наличия паттерна
        if parser.pattern.lower() in text:
            # Кейс слово Эль + есть фрукты в тексте
            if parser.match_if_parsed_fruits:
                if not (style_fruits := _parse_fruits(text)):
                    continue

            style = parser.parsed_style
            if parser.parse_hops:
                style_hops = _parse_hops(text)
            if parser.parse_fruits:
                style_fruits = _parse_fruits(text)

            break

    if not style:
        return None


    return BeerStyle(
        name=style,
        hops=style_hops,
        fruits=style_fruits,
    )


def _stem_text(text):
    stemmer = SnowballStemmer("russian")
    tokens = word_tokenize(text.lower())
    stemmed_words = [stemmer.stem(word) for word in tokens]
    text = " ".join(stemmed_words)
    return text


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
