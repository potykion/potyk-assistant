from pathlib import Path

import pytest

from kys_in_rest.beer.entities.beer_post import BeerStyle, BeerStyleName
from kys_in_rest.beer.features.parse_beer import parse_style


@pytest.mark.parametrize(
    "text_file, expected",
    [
        (
            "4BREWERS - TIPA.txt",
            BeerStyle(
                name=BeerStyleName.TIPA,
                hops=["Citra", "Citra Cryo", "Nectaron", "Hopburst Nectaron"],
            ),
        ),
        (
            "Midnight Project - Daily Quest.txt",
            BeerStyle(
                name=BeerStyleName.NE_IPA,
                hops=["Cascade NZ", "Pacifica Amplifire", "Rakau"],
            ),
        ),
        (
            "Brewlok - Сирин.txt",
            BeerStyle(
                name=BeerStyleName.SOUR_ALE, fruits=["груша", "манго", "маракуйя"]
            ),
        ),
        ("On The Bones - Токсовский Трамплин.txt", BeerStyle(name=BeerStyleName.IPA)),
        (
            "Khoffner - Неизбежность.txt",
            BeerStyle(name=BeerStyleName.SOUR_ALE, fruits=["вишня", "карамель"]),
        ),
        (
            "Lost Meadery - Аллергия.txt",
            BeerStyle(name=BeerStyleName.MEAD, fruits=["абрикос"]),
        ),
        (
            "4BREWERS - How to Human.txt",
            BeerStyle(
                name=BeerStyleName.SOUR_ALE, fruits=['апельсин', 'корица', 'облепиха']
            ),
        ),
        (
            "Chibis - Ачивка.txt",
            BeerStyle(
                name=BeerStyleName.NE_IPA, hops=["Citra", "Green Bullet", "Superdelic"]
            ),
        ),
        (
            "Brewmen - Первый полет на метле.txt",
            BeerStyle(name=BeerStyleName.MILK_STOUT),
        ),
        ("Plague - Trosdorf.txt", BeerStyle(name=BeerStyleName.WEIZEN)),
        (
            "Velka Morava - Mysterious Island.txt",
            BeerStyle(name=BeerStyleName.NE_IPA, hops=["Galaxy", "Mosaic"]),
        ),
        (
            "Rewort - Analog Dream.txt",
            BeerStyle(name=BeerStyleName.SOUR_ALE, fruits=['личи', 'малина', 'роза']),
        ),
        (
            "Plague - Vivid Vibe Ежевика.txt",
            BeerStyle(name=BeerStyleName.BERLINER, fruits=["ежевика"]),
        ),
        (
            "4BREWERS - Когда Ницше плакал.txt",
            BeerStyle(
                name=BeerStyleName.SOUR_ALE,
                fruits=['малина', 'ревень', 'черная смородина'],
            ),
        ),
        (
            "Chibis - Hop Port Dock 5.txt",
            BeerStyle(name=BeerStyleName.IPA, hops=["Citra", "Galaxy"]),
        ),
        (
            "Brewmen - Berry Cookie.txt",
            BeerStyle(
                name=BeerStyleName.SOUR_ALE,
                fruits=['печенье', 'черная смородина', 'черника'],
            ),
        ),
    ],
)
def test_parse_style(text_file, expected):
    with open(
        Path(__file__).parent / "fixtures" / text_file, "r", encoding="utf-8"
    ) as f:
        text = f.read()

    assert parse_style(text) == expected
