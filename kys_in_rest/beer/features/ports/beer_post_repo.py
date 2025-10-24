import abc

from kys_in_rest.beer.entities.beer_post import BeerPost


class BeerPostRepo:
    @abc.abstractmethod
    def start_new_post(self) -> None:
        pass

    @abc.abstractmethod
    def update_post(self, post: BeerPost) -> None:
        pass

    @abc.abstractmethod
    def get_last_post(self) -> BeerPost:
        pass
