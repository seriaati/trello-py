from __future__ import annotations

from typing import Literal, TypeAlias

__all__ = ("CardPos", "LabelColor")

# Models
CardPos: TypeAlias = Literal["top", "bottom"]
LabelColor: TypeAlias = Literal[
    "yellow",
    "purple",
    "blue",
    "red",
    "green",
    "orange",
    "black",
    "sky",
    "pink",
    "lime",
    "green_light",
]

# Request
RequestMethod: TypeAlias = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

# OAuth
OAuthCallbackMethod: TypeAlias = Literal["postMessage", "fragment"]
OAuthScope: TypeAlias = Literal["read", "write", "account"]
OAuthExpiration: TypeAlias = Literal["1hour", "1day", "30days", "never"]
