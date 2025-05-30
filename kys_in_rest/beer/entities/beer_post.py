import enum
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from kys_in_rest.core.tg_utils import tg_escape

hops = [
    "Cascade NZ",
    "Citra Cryo",
    "Citra",
    "Galaxy",
    "Green Bullet",
    "Hopburst Nectaron",
    "Mosaic CRYO",
    "Mosaic",
    "Nectaron",
    "Pacifica Amplifire",
    "Rakau",
    "Superdelic",
    "Vic Secret",
]

fruits = [
    ("абрикос", "абрикос"),
    ("апельсин", "апельсин"),
    ("ананас", "ананас"),
    ("мандарин", "мандарин"),
    ("вишн", "вишня"),
    ("груш", "груша"),
    ("ежевик", "ежевика"),
    ("карамел", "карамель"),
    ("кориц", "корица"),
    ("лич", "личи"),
    ("малин", "малина"),
    ("манг", "манго"),
    ("маракуй", "маракуйя"),
    ("облепих", "облепиха"),
    ("печен", "печенье"),
    ("ревен", "ревень"),
    ("роз", "роза"),
    ("черн смородин", "черная смородина"),
    ("черник", "черника"),
    ("ванил", "ваниль"),
    ("мелисс", "мелисса"),
    ("raspberry", "малина"),
    ("passion fruit", "маракуйя"),
    ("melissa", "мелисса"),
    ("каламанс", "каламанси"),
]


class BeerStyleName(enum.StrEnum):
    TIPA = "TIPA"
    DIPA = "DIPA"
    NE_IPA = "NE IPA"
    IPA = "IPA"
    MEAD = "Mead"
    SOUR_ALE = "Sour Ale"
    BERLINER = "Berliner"
    MILK_STOUT = "Milk Stout"
    WEIZEN = "Weizen"
    LAGER = "Lager"
    HELLES = "Helles"
    NON_ALCO_LAGER = "Non-Alco Lager"


class BeerStyle(BaseModel):
    name: BeerStyleName | str
    hops: list[str] = Field(default_factory=list)
    fruits: list[str] = Field(default_factory=list)

    def make_style_line(self) -> str:
        name = tg_escape(str(self.name))
        if self.hops:
            return f"{name} w/ {', '.join(self.hops)}"
        elif self.fruits:
            return f"{name} w/ {', '.join(self.fruits)}"
        else:
            return name


class BeerLine(BaseModel):
    name: str
    brewery: str
    style: BeerStyle
    link: str

    @property
    def style_icon(self) -> str:
        if self.style.name == BeerStyleName.MEAD:
            return "🍯"
        else:
            return "🍺"

    def make_beer_line(self) -> str:
        brewery_w_name = tg_escape(f"{self.brewery} — {self.name}")
        return f"{self.style_icon} [{brewery_w_name}]({self.link}) • _{self.style.make_style_line()}_"


class BeerPost(BaseModel):
    id: int = Field(default=0)
    created: datetime = Field(default_factory=datetime.utcnow)
    beers: list[BeerLine] = Field(default_factory=list)

    def make_post_text(self) -> str:
        return "\n".join(
            [
                "*Новинки*",
                *sorted(beer.make_beer_line() for beer in self.beers),
            ]
        )
