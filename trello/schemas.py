from __future__ import annotations

from pydantic import BaseModel, Field, PositiveInt

from .types import TrelloCardPos, TrelloLabelColor

__all__ = ("TrelloCardCreate", "TrelloCardUpdate", "TrelloLabelCreate")


class TrelloCardCreate(BaseModel):
    name: str
    idList: str = Field(alias="list_id")

    desc: str | None = Field(alias="description", default=None)
    pos: TrelloCardPos | PositiveInt | None = Field(alias="position", default=None)
    closed: bool | None = Field(default=None)
    dueComplete: bool | None = Field(alias="completed", default=None)
    labels: list[str] | None = Field(default=None)


class TrelloCardUpdate(BaseModel):
    id: str

    name: str | None = Field(default=None)
    desc: str | None = Field(alias="description", default=None)
    pos: TrelloCardPos | PositiveInt | None = Field(alias="position", default=None)
    closed: bool | None = Field(default=None)
    dueComplete: bool | None = Field(alias="completed", default=None)

    idList: str | None = Field(alias="list_id", default=None)


class TrelloLabelCreate(BaseModel):
    name: str
    color: TrelloLabelColor
    idBoard: str = Field(alias="board_id")
