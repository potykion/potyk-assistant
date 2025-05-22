import enum
from typing import NamedTuple, Any, Type, Callable, overload, TypeVar
import inspect

T = TypeVar("T")


class RegistryEntryType(enum.StrEnum):
    constant = enum.auto()
    callable = enum.auto()


class RegistryEntry(NamedTuple):
    name: str
    type: RegistryEntryType
    val: Any
    cache: bool = False


class IOC:
    def __init__(self):
        self.registry: dict[str | Type, RegistryEntry] = {}
        self.cache: dict[str | Type, Any] = {}

    def register_constant(self, name: str, val: str):
        self.registry[name] = RegistryEntry(name, RegistryEntryType.constant, val)

    def register_callable(self, name_or_type, callable_: Callable, *, cache=False):
        self.registry[name_or_type] = RegistryEntry(
            name_or_type, RegistryEntryType.callable, callable_, cache
        )

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

