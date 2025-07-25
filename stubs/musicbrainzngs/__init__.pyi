from typing import Any

def set_useragent(
    app: str,
    version: str,
    contact: str | None = ...,
) -> None: ...

def search_release_groups(
    *,
    artist: str | None = ..., 
    releasegroup: str | None = ..., 
    limit: int | None = ...,
) -> dict[str, Any]: ...

def get_release_group_by_id(
    id: str, 
    includes: list[str] | None = ...
) -> dict[str, Any]: ...