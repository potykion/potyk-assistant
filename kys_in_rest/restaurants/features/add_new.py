from kys_in_rest.core.tg_utils import AskForDataTg
from kys_in_rest.restaurants.features.ports import RestRepo


class AddNewRestaurant:
    def __init__(self, rest_repo: RestRepo) -> None:
        self.rest_repo = rest_repo

    def do(self):
        rest = self.rest_repo.get_or_create_draft()

        if not rest["name"]:
            raise AskForDataTg("Как называется?")

        # todo