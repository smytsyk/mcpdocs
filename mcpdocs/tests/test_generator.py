from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcpdocs.generator import McpDocs


@pytest.fixture
def mock_spec(full_server_spec):
    return full_server_spec


class TestMcpDocs:
    @pytest.mark.asyncio
    async def test_generate_calls_introspect_and_render(self, mock_spec):
        with patch("mcpdocs.generator.Introspector") as mock_introspector_cls:
            mock_introspector = mock_introspector_cls.return_value
            mock_introspector.introspect = AsyncMock(return_value=mock_spec)

            with patch("mcpdocs.generator.Renderer") as mock_renderer_cls:
                mock_renderer = mock_renderer_cls.return_value
                mock_renderer.render = MagicMock()

                docs = McpDocs(url="http://test/sse")
                await docs.generate(output_dir="./test-site")

                mock_introspector.introspect.assert_called_once()
                mock_renderer.render.assert_called_once_with(mock_spec, "./test-site")

    @pytest.mark.asyncio
    async def test_introspect_returns_spec(self, mock_spec):
        with patch("mcpdocs.generator.Introspector") as mock_introspector_cls:
            mock_introspector = mock_introspector_cls.return_value
            mock_introspector.introspect = AsyncMock(return_value=mock_spec)

            docs = McpDocs(url="http://test/sse")
            spec = await docs.introspect()

            assert spec == mock_spec
            mock_introspector.introspect.assert_called_once()
