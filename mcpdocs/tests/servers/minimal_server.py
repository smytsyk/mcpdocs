from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="minimal-test-server")
mcp._mcp_server.version = "0.1.0"


@mcp.tool()
async def ping() -> str:
    """Health check endpoint."""
    return "pong"


if __name__ == "__main__":
    mcp.run()
