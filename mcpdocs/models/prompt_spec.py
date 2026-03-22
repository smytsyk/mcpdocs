from pydantic import BaseModel, ConfigDict


class PromptArgument(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str | None = None
    required: bool = False


class PromptSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str | None = None
    arguments: list[PromptArgument] = []
