from mcpdocs.introspector import Introspector
from mcpdocs.models import ServerSpec
from mcpdocs.renderer import Renderer


class McpDocs:
    """Generate static HTML documentation for an MCP server.

    Args:
        url: SSE URL of the running MCP server (e.g. "http://localhost:8000/sse").
        timeout: Timeout in seconds for each MCP protocol call.
    """

    def __init__(
        self,
        url: str,
        timeout: float = 30.0,
    ) -> None:
        self._introspector = Introspector(
            url=url,
            timeout=timeout,
        )
        self._renderer = Renderer()

    async def introspect(self) -> ServerSpec:
        """Connect to the MCP server and return its full capability spec."""
        return await self._introspector.introspect()

    async def generate(self, output_dir: str) -> ServerSpec:
        """Introspect the MCP server and generate static HTML docs.

        Args:
            output_dir: Directory to write the generated HTML files.

        Returns:
            The introspected ServerSpec.
        """
        spec = await self._introspector.introspect()
        self._renderer.render(spec, output_dir)
        return spec
