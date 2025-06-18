import enum
import logging
from typing import (
    NamedTuple,
    Any,
    Type,
    Callable,
    overload,
    TypeVar,
    TypeAlias,
    Generic,
)
import inspect

T = TypeVar("T")
NameOrType: TypeAlias = str | Type[Any]


class RegistryEntryType(enum.StrEnum):
    constant = enum.auto()
    callable = enum.auto()


class RegistryEntry(Generic[T], NamedTuple):
    name: NameOrType
    type: RegistryEntryType
    val: Any
    cache: bool = False
    teardown: Callable[[T], None] | None = None


class IOC:
    def __init__(self) -> None:
        self.registry: dict[NameOrType, RegistryEntry[Any]] = {}
        self.cache: dict[NameOrType, Any] = {}

    def register(
        self,
        name_or_type: NameOrType,
        val: Any,
        *,
        cache: bool = False,
        teardown: Callable[[Any], None] | None = None,
    ) -> None:
        if callable(val):
            type_ = RegistryEntryType.callable
        else:
            type_ = RegistryEntryType.constant

        self.registry[name_or_type] = RegistryEntry(
            name_or_type,
            type_,
            val,
            cache,
            teardown,
        )

    def teardown(self) -> None:
        for entry in self.registry.values():
            if entry.teardown:
                resolved = self.resolve(entry.name)
                entry.teardown(resolved)

    @overload
    def resolve(self, name_or_type: Type[T]) -> T: ...
    @overload
    def resolve(self, name_or_type: str) -> Any: ...

    def resolve(self, name_or_type: NameOrType) -> Any:
        try:
            entry = self.registry[name_or_type]
        except KeyError:
            logging.warning(
                f"{name_or_type=} is not registered; creating entry w val=name_or_type..."
            )
            entry = self.make_yolo_entry(name_or_type)

        if entry.type == RegistryEntryType.constant:
            return entry.val
        elif entry.type == RegistryEntryType.callable:
            if entry.cache:
                if cached := self.cache.get(name_or_type):
                    return cached

            resolved_params: dict[str, Any] = {}

            params = inspect.signature(entry.val).parameters
            for param_key, param_type in params.items():
                if param_key in self.registry:
                    resolved_params[param_key] = self.resolve(param_key)
                else:
                    resolved_params[param_key] = self.resolve(param_type.annotation)
            resolved = entry.val(**resolved_params)

            if entry.cache:
                self.cache[name_or_type] = resolved

            return resolved
        else:
            raise Exception(f"resolve don't support {entry.type=}")

    def make_yolo_entry(self, name_or_type: NameOrType) -> RegistryEntry[Any]:
        val = name_or_type
        if callable(val):
            type_ = RegistryEntryType.callable
        else:
            type_ = RegistryEntryType.constant

        return RegistryEntry(name_or_type, type_, val)
