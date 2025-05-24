from kys_in_rest.core.tg_utils import TgCbOption
from kys_in_rest.restaurants.entries.metro import metro_colors


def list_metro_items() -> list[TgCbOption]:
    metro_items = [
        TgCbOption(f"{color} {metro}", metro)
        for metro, color in sorted(metro_colors.items(), key=lambda item: item[1])
    ]
    return metro_items
