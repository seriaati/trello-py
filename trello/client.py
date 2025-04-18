from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import aiohttp
from loguru import logger
from yarl import URL

from trello.errors import raise_for_status_code

from .models import TrelloBoard, TrelloCard, TrelloLabel, TrelloList

if TYPE_CHECKING:
    from .schemas import TrelloCardCreate, TrelloCardUpdate, TrelloLabelCreate
    from .types import RequestMethod

__all__ = ("TrelloAPI",)


class TrelloAPI:
    def __init__(self, *, api_key: str, api_token: str) -> None:
        self._session: aiohttp.ClientSession | None = None
        self._base_url = URL("https://api.trello.com/1/")

        self.__api_key = api_key
        self.__api_token = api_token

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            msg = "Session is not initialized."
            raise ValueError(msg)

        return self._session

    async def _request(
        self, endpoint: str, *, method: RequestMethod = "GET", params: dict[str, Any] | None = None
    ) -> Any:
        logger.debug(f"{method} {endpoint} with {params=}")

        params = params or {}
        params["key"] = self.__api_key
        params["token"] = self.__api_token

        for key, value in params.items():
            if value is None:
                params.pop(key)
            elif isinstance(value, bool):
                params[key] = str(value).lower()
            elif isinstance(value, list):
                params[key] = ",".join(map(str, value))

        async with self.session.request(method, self._base_url / endpoint, params=params) as resp:
            if not str(resp.status).startswith("2"):
                raise_for_status_code(resp.status)
            return await resp.json()

    async def start(self) -> None:
        if self._session is not None:
            return

        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def get_boards(self) -> list[TrelloBoard]:
        endpoint = "members/me/boards"
        data = await self._request(endpoint)
        return [TrelloBoard(**board) for board in data]

    async def get_board_lists(self, board_id: str) -> list[TrelloList]:
        endpoint = f"boards/{board_id}/lists"
        data = await self._request(endpoint)
        return [TrelloList(**board_list) for board_list in data]

    async def get_board_labels(self, board_id: str) -> list[TrelloLabel]:
        endpoint = f"boards/{board_id}/labels"
        data = await self._request(endpoint)
        return [TrelloLabel(**label) for label in data]

    async def get_list_cards(self, list_id: str) -> list[TrelloCard]:
        endpoint = f"lists/{list_id}/cards"
        data = await self._request(endpoint)
        return [TrelloCard(**card) for card in data]

    async def create_card(self, create: TrelloCardCreate) -> TrelloCard:
        endpoint = "cards"
        data = await self._request(
            endpoint, method="POST", params=create.model_dump(exclude_unset=True)
        )
        return TrelloCard(**data)

    async def update_card(self, update: TrelloCardUpdate) -> TrelloCard:
        endpoint = f"cards/{update.id}"
        data = await self._request(
            endpoint, method="PUT", params=update.model_dump(exclude_unset=True)
        )
        return TrelloCard(**data)

    async def delete_card(self, card_id: str) -> None:
        endpoint = f"cards/{card_id}"
        await self._request(endpoint, method="DELETE")

    async def create_label(self, create: TrelloLabelCreate) -> TrelloLabel:
        endpoint = "labels"
        data = await self._request(
            endpoint, method="POST", params=create.model_dump(exclude_unset=True)
        )
        return TrelloLabel(**data)

    async def delete_label(self, label_id: str) -> None:
        endpoint = f"labels/{label_id}"
        await self._request(endpoint, method="DELETE")
