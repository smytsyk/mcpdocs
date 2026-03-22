from datetime import UTC, datetime

import pytest

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


@pytest.fixture
def full_server_spec() -> ServerSpec:
    return ServerSpec(
        server_info=ServerInfo(
            name="test-server",
            version="2.0.0",
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
                name="list_items",
                description="List all items with pagination.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "default": 100,
                            "description": "Max items to return",
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "Number of items to skip",
                        },
                    },
                },
                annotations=ToolAnnotations(read_only=True),
            ),
            ToolSpec(
                name="delete_item",
                description="Delete an item by ID.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The item ID",
                        },
                    },
                    "required": ["item_id"],
                },
                annotations=ToolAnnotations(destructive=True),
            ),
        ],
        resources=[
            ResourceSpec(
                uri="config://settings",
                name="settings",
                description="Application settings",
                mime_type="application/json",
            ),
        ],
        resource_templates=[
            ResourceTemplateSpec(
                uri_template="data://{collection}/{id}",
                name="data_item",
                description="Get item from collection",
                mime_type="application/json",
            ),
        ],
        prompts=[
            PromptSpec(
                name="debug_error",
                description="Help debug an error message.",
                arguments=[
                    PromptArgument(
                        name="error", description="The error message", required=True
                    ),
                    PromptArgument(
                        name="context", description="Additional context", required=False
                    ),
                ],
            ),
        ],
        generated_at=datetime(2026, 1, 15, 10, 30, 0, tzinfo=UTC),
    )


@pytest.fixture
def minimal_server_spec() -> ServerSpec:
    return ServerSpec(
        server_info=ServerInfo(
            name="minimal-server",
            version=None,
            protocol_version="2025-06-18",
        ),
        capabilities=ServerCapabilities(
            tools=True,
            resources=False,
            prompts=False,
        ),
        tools=[
            ToolSpec(
                name="ping",
                description="Health check.",
                input_schema={"type": "object"},
                annotations=None,
            ),
        ],
        resources=[],
        resource_templates=[],
        prompts=[],
        generated_at=datetime(2026, 1, 15, 10, 30, 0, tzinfo=UTC),
    )
