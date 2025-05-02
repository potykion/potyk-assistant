from pathlib import Path

import pytest

from kys_in_rest.beer.features.parse_beer import parse_style


@pytest.mark.parametrize(
    "text_file, expected",
    [
        (
            "4BREWERS - TIPA.txt",
            "TIPA w/ Citra, Citra Cryo, Nectaron, Hopburst Nectaron",
        ),
        (
            "Midnight Project - Daily Quest.txt",
            "NE IPA w/ Cascade NZ, Pacifica Amplifire, Rakau",
        ),
        (
            "Brewlok - Сирин.txt",
            "Sour Ale w/ груша, манго, маракуйя",
        ),
        (
            "On The Bones - Токсовский Трамплин.txt",
            "IPA",
        ),
        (
            "Khoffner - Неизбежность.txt",
            "Sour Ale w/ вишня, карамель",
        ),
        (
            "Lost Meadery - Аллергия.txt",
            "Mead w/ абрикос",
        ),
        (
            "4BREWERS - How to Human.txt",
            "Sour Ale w/ апельсин, облепиха, корица",
        ),  (
            "Chibis - Ачивка.txt",
            "NE IPA w/ Citra, Green Bullet, Superdelic",
        ),
    ],
)
def test_parse_style(text_file, expected):
    with open(
        Path(__file__).parent / "fixtures" / text_file, "r", encoding="utf-8"
    ) as f:
        text = f.read()

    assert parse_style(text) == expected
