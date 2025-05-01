from kys_in_rest.core.tg_utils import TgFeature


class AddNewBeer(TgFeature):
    def do(self, text: str | None, tg_user_id: int) -> str:
        pass