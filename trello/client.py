from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import aiohttp

from .models import TrelloBoard, TrelloCard, TrelloLabel, TrelloList

if TYPE_CHECKING:
    from .schemas import TrelloCardCreate, TrelloCardUpdate, TrelloLabelCreate

__all__ = ("TrelloAPI",)


class TrelloAPI:
    def __init__(self, *, api_key: str, api_token: str) -> None:
        self._session: aiohttp.ClientSession | None = None

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
        self, url: str, *, method: str = "GET", params: dict[str, Any] | None = None
    ) -> Any:
        params = params or {}
        params["key"] = self.__api_key
        params["token"] = self.__api_token

        for key, value in params.items():
            if isinstance(value, bool):
                params[key] = str(value).lower()

        async with self.session.request(method, url, params=params) as resp:
            resp.raise_for_status()
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
        url = "https://api.trello.com/1/members/me/boards"
        data = await self._request(url)
        return [TrelloBoard(**board) for board in data]

    async def get_board_lists(self, board_id: str) -> list[TrelloList]:
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        data = await self._request(url)
        return [TrelloList(**board_list) for board_list in data]

    async def get_board_labels(self, board_id: str) -> list[TrelloLabel]:
        url = f"https://api.trello.com/1/boards/{board_id}/labels"
        data = await self._request(url)
        return [TrelloLabel(**label) for label in data]

    async def get_list_cards(self, list_id: str) -> list[TrelloCard]:
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        data = await self._request(url)
        return [TrelloCard(**card) for card in data]

    async def create_card(self, create: TrelloCardCreate) -> TrelloCard:
        url = "https://api.trello.com/1/cards"
        data = await self._request(url, method="POST", params=create.model_dump(exclude_unset=True))
        return TrelloCard(**data)

    async def update_card(self, update: TrelloCardUpdate) -> TrelloCard:
        url = f"https://api.trello.com/1/cards/{update.id}"
        data = await self._request(url, method="PUT", params=update.model_dump(exclude_unset=True))
        return TrelloCard(**data)

    async def create_label(self, create: TrelloLabelCreate) -> TrelloLabel:
        url = "https://api.trello.com/1/labels"
        data = await self._request(url, method="POST", params=create.model_dump(exclude_unset=True))
        return TrelloLabel(**data)

    async def delete_label(self, label_id: str) -> None:
        url = f"https://api.trello.com/1/labels/{label_id}"
        await self._request(url, method="DELETE")
