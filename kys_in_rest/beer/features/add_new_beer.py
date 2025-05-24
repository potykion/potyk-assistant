import os
from typing import cast

from kys_in_rest.beer.entities.beer_post import BeerPost, BeerLine
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo
from kys_in_rest.beer.features.parse_beer import parse_style
from kys_in_rest.core.tg_utils import (
    TgFeature,
    SendTgMessageInterrupt,
    AskForData,
    TgMsgToSend,
)
from kys_in_rest.tg.entities.input_tg_msg import InputTgMsg


class AddNewBeer(TgFeature):
    def __init__(self, beer_post_repo: BeerPostRepo) -> None:
        self.beer_post_repo = beer_post_repo

    def do(self, msg: InputTgMsg) -> str:
        if int(msg.tg_user_id) != int(os.environ["TG_ADMIN"]):
            raise SendTgMessageInterrupt(TgMsgToSend("Тебе нельзя"))

        if not msg.text and not msg.forward_link:
            self.beer_post_repo.start_new_post()
            raise AskForData(
                TgMsgToSend(
                    "Собираем пост. Алгоритм такой: форвардни пост про пиво, напиши название и продолжай пока не закончишь. "
                    "Вызови команду /new_beer для того чтобы начать пост заново."
                )
            )
        else:
            beer_post: BeerPost = self.beer_post_repo.get_last_post()

        if msg.forward_link:
            style = parse_style(cast(str, msg.text))
            if not style:
                raise AskForData(TgMsgToSend("Не удалось распарсить стиль((("))

            beer_post.beers.append(
                BeerLine(
                    name="",
                    brewery=cast(str, msg.forward_channel_name),
                    style=style,
                    link=msg.forward_link,
                )
            )
            self.beer_post_repo.update_post(beer_post)
            raise AskForData(TgMsgToSend("Как называется пив?"))
        else:
            beer_post.beers[-1].name = cast(str, msg.text)
            self.beer_post_repo.update_post(beer_post)
            return beer_post.make_post_text()
