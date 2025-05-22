import enum
from typing import NamedTuple, Any, Type, Callable, overload, TypeVar
import inspect

T = TypeVar("T")
NameOrType = str | Type


class RegistryEntryType(enum.StrEnum):
    constant = enum.auto()
    callable = enum.auto()


class RegistryEntry(NamedTuple):
    name: NameOrType
    type: RegistryEntryType
    val: Any
    cache: bool = False
    teardown: Callable | None = None


class IOC:
    def __init__(self):
        self.registry: dict[NameOrType, RegistryEntry] = {}
        self.cache: dict[NameOrType, Any] = {}

    def register(
        self,
        name_or_type,
        val: Any,
        *,
        cache=False,
        teardown: Callable | None = None,
    ):
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

    def teardown(self):
        for entry in self.registry.values():
            if entry.teardown:
                resolved = self.resolve(entry.name)
                entry.teardown(resolved)

    @overload
    def resolve(self, name_or_type: Type[T]) -> T: ...
    @overload
    def resolve(self, name_or_type: str) -> Any: ...

    def resolve(self, name_or_type):
        entry = self.registry[name_or_type]
        if entry.type == RegistryEntryType.constant:
            return entry.val
        elif entry.type == RegistryEntryType.callable:
            if entry.cache:
                if cached := self.cache.get(name_or_type):
                    return cached

            resolved_params = {}

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
