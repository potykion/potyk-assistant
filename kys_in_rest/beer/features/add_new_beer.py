import os

from kys_in_rest.beer.entities import beer_post
from kys_in_rest.beer.entities.beer_post import BeerPost, BeerLine, BeerStyle
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.features.parse_beer import parse_style
from kys_in_rest.core.tg_utils import TgFeature, SendTgMessageInterrupt, AskForData
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddNewBeer(TgFeature):
    def __init__(self, beer_post_repo: BeerPostRepo):
        self.beer_post_repo = beer_post_repo

    def do(
        self,
        _: str | None,
        tg_user_id: int,
        msg: InputTgMsg | None = None,
    ) -> str:
        if int(tg_user_id) != int(os.environ["TG_ADMIN"]):
            raise SendTgMessageInterrupt("Тебе нельзя")

        if not msg:
            self.beer_post_repo.start_new_post()
            raise AskForData(
                "Собираем пост. Алгоритм такой: форвардни пост про пиво, напиши название и продолжай пока не закончишь. "
                "Вызови команду /new_beer для того чтобы начать пост заново."
            )
        else:
            beer_post: BeerPost = self.beer_post_repo.get_last_post()

        if msg.forward_link:
            beer_post.beers.append(
                BeerLine(
                    name="",
                    brewery=msg.forward_channel_name,
                    style=parse_style(msg.text),
                    link=msg.forward_link,
                )
            )
            self.beer_post_repo.update_post(beer_post)
            raise AskForData("Как называется пив?")
        else:
            beer_post.beers[-1].name = msg.text
            self.beer_post_repo.update_post(beer_post)
            return beer_post.make_post_text()
