from unittest.mock import AsyncMock, patch

import mcp.types as types
import pytest

from mcpdocs.introspector import Introspector


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.initialize.return_value = types.InitializeResult(
        protocolVersion="2024-11-05",
        capabilities=types.ServerCapabilities(
            tools=types.ToolsCapability(),
            resources=types.ResourcesCapability(),
            prompts=types.PromptsCapability(),
        ),
        serverInfo=types.Implementation(name="test-server", version="1.0.0"),
    )

    session.list_tools.return_value = types.ListToolsResult(
        tools=[
            types.Tool(
                name="test_tool",
                description="A test tool",
                inputSchema={"type": "object"},
            )
        ]
    )

    session.list_resources.return_value = types.ListResourcesResult(
        resources=[
            types.Resource(
                uri="test://resource",
                name="test_resource",
                description="A test resource",
                mimeType="text/plain",
            )
        ]
    )

    session.list_resource_templates.return_value = types.ListResourceTemplatesResult(
        resourceTemplates=[]
    )

    session.list_prompts.return_value = types.ListPromptsResult(
        prompts=[
            types.Prompt(
                name="test_prompt",
                description="A test prompt",
                arguments=[],
            )
        ]
    )

    return session


class TestIntrospector:
    @pytest.mark.asyncio
    async def test_introspect_success(self, mock_session):
        # We need to mock the context manager sse_client
        mock_streams = (AsyncMock(), AsyncMock())

        with patch("mcpdocs.introspector.sse_client") as mock_sse:
            mock_sse.return_value.__aenter__.return_value = mock_streams

            with patch("mcpdocs.introspector.ClientSession") as mock_client_session:
                mock_client_session.return_value.__aenter__.return_value = mock_session

                introspector = Introspector(url="http://test/sse")
                spec = await introspector.introspect()

                assert spec.server_info.name == "test-server"
                assert len(spec.tools) == 1
                assert spec.tools[0].name == "test_tool"
                assert len(spec.resources) == 1
                assert spec.resources[0].name == "test_resource"
                assert len(spec.prompts) == 1
                assert spec.prompts[0].name == "test_prompt"

    @pytest.mark.asyncio
    async def test_introspect_failure(self):
        with patch("mcpdocs.introspector.sse_client") as mock_sse:
            mock_sse.side_effect = Exception("Connection refused")

            introspector = Introspector(url="http://test/sse")
            from mcpdocs.exceptions import IntrospectionError

            with pytest.raises(IntrospectionError):
                await introspector.introspect()
