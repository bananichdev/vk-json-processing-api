from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from utils.enums import StateEnum


class AppOperationOK(BaseModel):
    kind: Annotated[str, Field(max_length=32)]
    app_id: UUID


class AppState(BaseModel):
    state: StateEnum


class App(AppOperationOK, AppState):
    name: Annotated[str, Field(max_length=128)]
    version: Annotated[str, Field(regex=r"^\d+\.\d+\.\d+$")]
    description: Annotated[str, Field(max_length=4096)]
    json_data: dict | None = Field(alias="json")
