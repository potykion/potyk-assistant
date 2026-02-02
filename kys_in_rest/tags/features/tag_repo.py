import abc

from kys_in_rest.tags.entities.tag import Tag


class TagRepo(abc.ABC):
    @abc.abstractmethod
    def list_tags(self, entity_type: str | None = None) -> list[Tag]: ...
