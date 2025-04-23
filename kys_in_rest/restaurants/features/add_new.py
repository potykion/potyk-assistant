from kys_in_rest.core.tg_utils import AskForData
from kys_in_rest.restaurants.entries.restaurant import Restaurant
from kys_in_rest.restaurants.features.ports import RestRepo


class AddNewRestaurant:
    def __init__(self, rest_repo: RestRepo) -> None:
        self.rest_repo = rest_repo

    def do(self, text: str = None):
        rest, _ = self.rest_repo.get_or_create_draft()
        rest: Restaurant

        params_and_questions = [
            ("name", "Как называется?"),
            # todo
            # ("yandex_maps", "Скинь ссылку на Яндекс Карты"),
            # ("metro", "Какое метро?"),
        ]

        for field, question in params_and_questions:
            if not rest.get(field):
                if text:
                    rest[field] = text
                    self.rest_repo.update_draft(rest)
                else:
                    raise AskForData(question, field)

        rest["draft"] = False
        self.rest_repo.update_draft(rest)

        return rest
