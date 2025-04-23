import re


def split_strip(str_, sep=","):
    """
    >>> split_strip("a, b")
    ['a', 'b']
    """
    return [item.strip() for item in str_.split(sep)]


def parse_link(text: str) -> str | None:
    """
    >>> parse_link('''Smoke is
    ... 3-я ул. Ямского Поля, 2, корп. 5
    ... https://yandex.ru/maps/org/smoke_is/224290958595?si=potyk-io''')
    'https://yandex.ru/maps/org/smoke_is/224290958595?si=potyk-io'
    """

    return match.group(0) if (match := re.search(r"(https?://[^\s]+)", text)) else None
