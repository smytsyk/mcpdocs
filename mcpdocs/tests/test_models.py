from datetime import UTC, datetime

from mcpdocs.models import (
    PromptArgument,
    PromptSpec,
    ResourceSpec,
    ResourceTemplateSpec,
    ServerCapabilities,
    ServerInfo,
    ServerSpec,
    ToolAnnotations,
    ToolSpec,
)


class TestToolSpec:
    def test_create_tool_spec(self) -> None:
        tool = ToolSpec(
            name="list_items",
            description="List all items",
            input_schema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10},
                },
            },
            annotations=None,
        )
        assert tool.name == "list_items"
        assert tool.description == "List all items"
        assert tool.input_schema["type"] == "object"

    def test_tool_spec_with_annotations(self) -> None:
        annotations = ToolAnnotations(
            read_only=True,
            destructive=False,
            idempotent=True,
            open_world=None,
        )
        tool = ToolSpec(
            name="get_item",
            description=None,
            input_schema={"type": "object"},
            annotations=annotations,
        )
        assert tool.annotations is not None
        assert tool.annotations.read_only is True
        assert tool.annotations.destructive is False

    def test_tool_spec_serialization(self) -> None:
        tool = ToolSpec(
            name="test",
            description="desc",
            input_schema={"type": "object"},
            annotations=None,
        )
        data = tool.model_dump(mode="json")
        assert data["name"] == "test"
        roundtrip = ToolSpec.model_validate(data)
        assert roundtrip == tool


class TestResourceSpec:
    def test_create_resource_spec(self) -> None:
        resource = ResourceSpec(
            uri="file:///data/config.json",
            name="config",
            description="Configuration file",
            mime_type="application/json",
        )
        assert resource.uri == "file:///data/config.json"
        assert resource.mime_type == "application/json"

    def test_resource_spec_optional_fields(self) -> None:
        resource = ResourceSpec(
            uri="custom://data",
            name="data",
            description=None,
            mime_type=None,
        )
        assert resource.description is None
        assert resource.mime_type is None


class TestResourceTemplateSpec:
    def test_create_resource_template(self) -> None:
        template = ResourceTemplateSpec(
            uri_template="file:///data/{name}.json",
            name="data_file",
            description="Data file by name",
            mime_type="application/json",
        )
        assert "{name}" in template.uri_template


class TestPromptSpec:
    def test_create_prompt_spec(self) -> None:
        prompt = PromptSpec(
            name="debug_error",
            description="Debug an error",
            arguments=[
                PromptArgument(
                    name="error_message", description="The error", required=True
                ),
                PromptArgument(name="context", description=None, required=False),
            ],
        )
        assert prompt.name == "debug_error"
        assert len(prompt.arguments) == 2
        assert prompt.arguments[0].required is True
        assert prompt.arguments[1].required is False

    def test_prompt_spec_no_arguments(self) -> None:
        prompt = PromptSpec(
            name="help",
            description="Show help",
            arguments=[],
        )
        assert prompt.arguments == []


class TestServerSpec:
    def test_create_full_server_spec(self) -> None:
        spec = ServerSpec(
            server_info=ServerInfo(
                name="test-server",
                version="1.0.0",
                protocol_version="2025-06-18",
            ),
            capabilities=ServerCapabilities(
                tools=True,
                resources=True,
                prompts=True,
                logging=False,
                subscriptions=False,
            ),
            tools=[
                ToolSpec(
                    name="echo",
                    description="Echo input",
                    input_schema={"type": "object"},
                    annotations=None,
                ),
            ],
            resources=[],
            resource_templates=[],
            prompts=[],
            generated_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        assert spec.server_info.name == "test-server"
        assert spec.capabilities.tools is True
        assert len(spec.tools) == 1
        assert spec.tools[0].name == "echo"

    def test_server_spec_json_roundtrip(self) -> None:
        spec = ServerSpec(
            server_info=ServerInfo(
                name="s",
                version=None,
                protocol_version="2025-06-18",
            ),
            capabilities=ServerCapabilities(
                tools=True,
                resources=False,
                prompts=False,
                logging=False,
                subscriptions=False,
            ),
            tools=[],
            resources=[],
            resource_templates=[],
            prompts=[],
            generated_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        data = spec.model_dump(mode="json")
        roundtrip = ServerSpec.model_validate(data)
        assert roundtrip.server_info.name == "s"
        assert roundtrip.server_info.version is None
