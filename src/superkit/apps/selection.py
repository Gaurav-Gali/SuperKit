def resolve_apps(
    *,
    include_all: bool,
    include: list[str] | None,
    exclude: list[str] | None,
    discovered: set[str],
) -> list[str]:
    include = set(include or [])
    exclude = set(exclude or [])

    if include_all and include:
        raise ValueError(
            "Cannot use `include_all=True` together with `include`"
        )

    if include_all:
        selected = set(discovered)
    else:
        if not include:
            raise ValueError(
                "Either `include_all=True` or `include=[...]` must be provided"
            )
        selected = include

    unknown = selected - discovered
    if unknown:
        raise ValueError(f"Unknown apps: {sorted(unknown)}")

    final = selected - exclude

    if not final:
        raise ValueError("No apps left to mount after exclusions")

    return sorted(final)
