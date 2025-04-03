from __future__ import annotations

import random
from typing import TYPE_CHECKING, get_args

from yarl import URL

from .types import TrelloLabelColor

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .types import OAuthCallbackMethod, OAuthExpiration, OAuthScope

__all__ = ("generate_oauth_url", "get_random_label_color")


def generate_oauth_url(
    *,
    callback_method: OAuthCallbackMethod,
    return_url: str,
    scopes: Sequence[OAuthScope],
    expiration: OAuthExpiration,
    key: str,
) -> str:
    base = URL("https://trello.com/1/authorize")
    params = {
        "key": key,
        "return_url": return_url,
        "callback_method": callback_method,
        "expiration": expiration,
        "scope": ",".join(scopes),
    }
    return str(base.with_query(params))


def get_random_label_color() -> TrelloLabelColor:
    colors = get_args(TrelloLabelColor)
    return random.choice(colors)
