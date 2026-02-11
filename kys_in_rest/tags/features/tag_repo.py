import abc

from kys_in_rest.tags.entities.tag import Tag


class TagRepo(abc.ABC):
    @abc.abstractmethod
    def list_tags(self, entity_type: str | None = None) -> list[Tag]: ...

    @abc.abstractmethod
    def get_tag_ids_for_entity(self, entity_id: int, entity_type: str) -> list[int]: ...

    @abc.abstractmethod
    def set_tags_for_entity(self, entity_id: int, entity_type: str, tag_ids: list[int]) -> None: ...
