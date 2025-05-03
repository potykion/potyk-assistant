import enum
from datetime import datetime

from pydantic import BaseModel, Field

from kys_in_rest.core.tg_utils import escape

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
    "Galaxy",
    "Mosaic",
]

fruits = [
    ("абрикос", "абрикос"),
    ("апельсин", "апельсин"),
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
]


class BeerStyleName(enum.StrEnum):
    TIPA = "TIPA"
    NE_IPA = "NE IPA"
    IPA = "IPA"
    MEAD = "Mead"
    SOUR_ALE = "Sour Ale"
    BERLINER = "Berliner"
    MILK_STOUT = "Milk Stout"
    WEIZEN = "Weizen"


class BeerStyle(BaseModel):
    name: BeerStyleName | str
    hops: list[str] = Field(default_factory=list)
    fruits: list[str] = Field(default_factory=list)

    def make_style_line(self):
        if self.hops:
            return f"{self.name} w/ {', '.join(self.hops)}"
        elif self.fruits:
            return f"{self.name} w/ {', '.join(self.fruits)}"
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
        brewery_w_name = escape(f"{self.brewery} — {self.name}")
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
