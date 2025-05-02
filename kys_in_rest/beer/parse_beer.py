from typing_extensions import NamedTuple

hops = [
    "Citra",
    "Citra Cryo",
    "Nectaron",
    "Hopburst Nectaron",
    "Cascade NZ",
    "Pacifica Amplifire",
    "Rakau",
    "Green Bullet",
    "Superdelic",
]

# todo use stemmer
fruits = [
    ("грушей", "груша"),
    ("манго", "манго"),
    ("маракуйей", "маракуйя"),
    ("вишня", "вишня"),
    ("карамель", "карамель"),
    ("абрикосы", "абрикос"),
    ("апельсина", "апельсин"),
    ("облепихи", "облепиха"),
    ("корицы", "корица"),
]


class StyleParser(NamedTuple):
    pattern: str
    parsed_style: str

    parse_hops: bool = False
    parse_fruits: bool = False
    # Кейс слово Эль + есть фрукты в тексте
    match_if_parsed_fruits: bool = False


style_parsers = [
    StyleParser("тройной индийский пэйл эль", "TIPA", parse_hops=True),
    StyleParser("NE IPA", "NE IPA", parse_hops=True),
    StyleParser("American IPA", "IPA", parse_hops=True),
    StyleParser("мид", "Mead", parse_fruits=True),
    StyleParser("саур эль", "Sour Ale", parse_fruits=True),
    StyleParser("Sour", "Sour Ale", parse_fruits=True),
    StyleParser("эль", "Sour Ale", parse_fruits=True, match_if_parsed_fruits=True),
]


def parse_name(text: str) -> str: ...


def parse_style(text: str) -> str:
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

    if style_hops:
        return f"{style} w/ {', '.join(style_hops)}"
    elif style_fruits:
        return f"{style} w/ {', '.join(style_fruits)}"
    else:
        return style


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
