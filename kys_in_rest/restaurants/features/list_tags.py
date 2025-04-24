from kys_in_rest.core.tg_utils import TgCbOption
from kys_in_rest.restaurants.entries.tag import tag_groups


def list_tag_items() -> list[TgCbOption]:
    return [
        TgCbOption(tag, cb_data=tag)
        for tags in tag_groups.values()
        for tag in tags
    ]
