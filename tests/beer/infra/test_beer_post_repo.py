from datetime import datetime

from kys_in_rest.beer.entities.beer_post import BeerLine, BeerStyle, BeerStyleName
from kys_in_rest.beer.features.beer_post_repo import BeerPostRepo


def test_SqliteBeerPostRepo(ioc):
    repo = ioc.resolve(BeerPostRepo)

    repo.start_new_post()
    post = repo.get_last_post()

    assert post is not None
    assert post.id is not None
    assert isinstance(post.created, datetime)

    line = BeerLine(
        name="",
        brewery="4BREWERS",
        style=BeerStyle(
            name=BeerStyleName.TIPA,
            hops=["Citra", "Citra Cryo", "Nectaron", "Hopburst Nectaron"],
            fruits=[],
        ),
        link="https://t.me/fourbrewers/1037",
    )
    post.beers.append(line)

    repo.update_post(post)
    post = repo.get_last_post()

    assert post is not None
    assert post.beers == [line]

    post.beers[-1].name = "Магнитные бури"
    repo.update_post(post)
    post = repo.get_last_post()

    assert post.beers[-1].name == "Магнитные бури"
