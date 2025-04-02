from __future__ import annotations

from typing import Literal, TypeAlias

__all__ = ("TrelloCardPos", "TrelloLabelColor")

TrelloCardPos: TypeAlias = Literal["top", "bottom"]
TrelloLabelColor: TypeAlias = Literal[
    "yellow", "purple", "blue", "red", "green", "orange", "black", "sky", "pink", "lime"
]
