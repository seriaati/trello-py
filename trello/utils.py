from __future__ import annotations

from typing import TYPE_CHECKING

from yarl import URL

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .types import OAuthCallbackMethod, OAuthExpiration, OAuthScope

__all__ = ("generate_oauth_url",)


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
