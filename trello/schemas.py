from __future__ import annotations

from pydantic import BaseModel, Field, PositiveInt

from .types import CardPos, LabelColor

__all__ = ("TrelloCardCreate", "TrelloCardUpdate", "TrelloLabelCreate")


class TrelloCardCreate(BaseModel):
    name: str
    idList: str = Field(alias="list_id")

    desc: str | None = Field(alias="description", default=None)
    pos: CardPos | PositiveInt | None = Field(alias="position", default=None)
    closed: bool | None = Field(default=None)
    dueComplete: bool | None = Field(alias="completed", default=None)
    idLabels: list[str] | None = Field(alias="label_ids", default=None)


class TrelloCardUpdate(BaseModel):
    id: str

    name: str | None = Field(default=None)
    desc: str | None = Field(alias="description", default=None)
    pos: CardPos | PositiveInt | None = Field(alias="position", default=None)
    closed: bool | None = Field(default=None)
    dueComplete: bool | None = Field(alias="completed", default=None)
    idLabels: list[str] | None = Field(alias="label_ids", default=None)

    idList: str | None = Field(alias="list_id", default=None)


class TrelloLabelCreate(BaseModel):
    name: str
    color: LabelColor
    idBoard: str = Field(alias="board_id")
