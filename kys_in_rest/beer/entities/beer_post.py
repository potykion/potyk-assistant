import dataclasses
import enum
from datetime import datetime
from typing import NamedTuple

from pydantic import BaseModel

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


class BeerStyleName(enum.StrEnum):
    TIPA = "TIPA"
    NE_IPA = "NE IPA"
    IPA = "IPA"
    MEAD = "Mead"
    SOUR_ALE = "Sour Ale"


class BeerStyle(BaseModel):
    name: BeerStyleName
    hops: list[str]
    fruits: list[str]

    def make_style_line(self):
        if self.hops:
            return f"{self.name} w/ {', '.join(self.hops)}"
        elif self.fruits:
            return f"{self.fruits} w/ {', '.join(self.fruits)}"
        else:
            return self.name


class BeerLine(BaseModel):
    name: str
    brewery: str
    style: BeerStyle
    link: str

    @property
    def style_icon(self):
        if self.style.name == BeerStyleName.MEAD:
            return "🍯"
        else:
            return "🍺"

    def make_beer_line(self):
        return f"{self.brewery} — {self.name} • _{self.style.make_style_line()}_"


class BeerPost(BaseModel):
    id: int
    created: datetime
    beers: list[BeerLine]

    @classmethod
    def new(cls):
        return BeerPost(
            id=0,
            created=datetime.utcnow(),
            beers=[],
        )

    def make_post_text(self) -> str:
        return "\n".join(
            [
                "*Новинки*",
                *(
                    f"{beer.style_icon} [{beer.make_beer_line()}]({beer.link})"
                    for beer in self.beers
                ),
            ]
        )
