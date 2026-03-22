from typing import Any

from pydantic import BaseModel, ConfigDict


class ToolAnnotations(BaseModel):
    model_config = ConfigDict(frozen=True)

    read_only: bool | None = None
    destructive: bool | None = None
    idempotent: bool | None = None
    open_world: bool | None = None


class ToolSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str | None = None
    input_schema: dict[str, Any]
    annotations: ToolAnnotations | None = None
