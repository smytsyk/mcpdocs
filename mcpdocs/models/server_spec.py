from datetime import datetime

from pydantic import BaseModel, ConfigDict

from mcpdocs.models.prompt_spec import PromptSpec
from mcpdocs.models.resource_spec import ResourceSpec, ResourceTemplateSpec
from mcpdocs.models.tool_spec import ToolSpec


class ServerInfo(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    version: str | None = None
    protocol_version: str


class ServerCapabilities(BaseModel):
    model_config = ConfigDict(frozen=True)

    tools: bool = False
    resources: bool = False
    prompts: bool = False
    logging: bool = False
    subscriptions: bool = False


class ServerSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    server_info: ServerInfo
    capabilities: ServerCapabilities
    tools: list[ToolSpec] = []
    resources: list[ResourceSpec] = []
    resource_templates: list[ResourceTemplateSpec] = []
    prompts: list[PromptSpec] = []
    generated_at: datetime
