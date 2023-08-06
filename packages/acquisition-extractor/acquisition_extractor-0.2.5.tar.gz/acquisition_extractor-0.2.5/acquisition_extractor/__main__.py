from pathlib import Path
from typing import Iterator, Optional

from .decisions import define_data
from .statutes import get_statute


def decode_statutes(parent: Path, context: str) -> Optional[Iterator[dict]]:
    """Given a parent directory "location" with a subfolder named "context",
    generate decision-like data from entries of the subfolder, or the grandchildren of the parent directory.

    Args:
        parent (Path): The parent local directory
        context (str): Possible options include "ra", "eo", "pd", "ca", "bp", "act", "const"

    Returns:
        Optional[Iterator[dict]]: [description]

    Yields:
        Iterator[Optional[Iterator[dict]]]: [description]
    """
    if context not in ["ra", "eo", "pd", "ca", "bp", "act", "const"]:
        return None

    folder = parent / "statutes"
    if not folder.exists():
        return None

    subfolder = folder / context
    if not subfolder.exists():
        return None

    for child in subfolder.glob("*"):
        yield get_statute(folder, child, context)


def decode_decisions(loc: Path, context: str) -> Optional[Iterator[dict]]:
    """Given a parent directory "location" with a subfolder named "context",
    generate decision-like data from entries of the subfolder, or the grandchildren of the parent directory.

    Args:
        loc (Path): The parent local directory
        context (str): Either "legacy" or "sc"

    Returns:
        Optional[Iterator[dict]]: [description]

    Yields:
        Iterator[Optional[Iterator[dict]]]: [description]
    """
    if context not in ["legacy", "sc"]:
        return None

    folder = loc / "decisions" / context
    if not folder.exists():
        return None

    locations = folder.glob("*")
    for location in locations:
        yield define_data(location)
