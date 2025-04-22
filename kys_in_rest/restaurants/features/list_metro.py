from kys_in_rest.restaurants.entries.metro import metro_colors


def list_metro_items():
    metro_items = sorted(metro_colors.items(), key=lambda item: item[1])
    metro_items = [
        (f"{color} {metro}", f"metro_{metro}") for metro, color in metro_items
    ]
    return metro_items
