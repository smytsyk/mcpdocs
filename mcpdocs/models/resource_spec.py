from pydantic import BaseModel, ConfigDict


class ResourceSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    uri: str
    name: str
    description: str | None = None
    mime_type: str | None = None


class ResourceTemplateSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    uri_template: str
    name: str
    description: str | None = None
    mime_type: str | None = None
