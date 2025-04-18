from __future__ import annotations

from pydantic import BaseModel, Field

from trello.types import LabelColor

__all__ = ("TrelloBoard", "TrelloCard", "TrelloLabel", "TrelloList")


class TrelloBoard(BaseModel):
    id: str
    name: str
    description: str = Field(alias="desc")
    url: str
    short_url: str = Field(alias="shortUrl")


class TrelloList(BaseModel):
    id: str
    name: str
    closed: bool
    position: float = Field(alias="pos")
    board_id: str = Field(alias="idBoard")


class TrelloCard(BaseModel):
    id: str
    name: str
    description: str = Field(alias="desc")
    short_url: str = Field(alias="shortUrl")
    url: str
    closed: bool
    position: float = Field(alias="pos")
    list_id: str = Field(alias="idList")
    board_id: str = Field(alias="idBoard")
    completed: bool = Field(alias="dueComplete")
    label_ids: list[str] = Field(alias="labels")


class TrelloLabel(BaseModel):
    id: str
    name: str
    color: LabelColor
    uses: int = Field(alias="uses")
    board_id: str = Field(alias="idBoard")
