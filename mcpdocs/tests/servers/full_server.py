from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="full-test-server")
mcp._mcp_server.version = "1.0.0"


@mcp.tool()
async def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


@mcp.tool()
async def add(a: int, b: int) -> str:
    """Add two numbers together."""
    return str(a + b)


@mcp.resource("config://app")
async def app_config() -> str:
    """Application configuration."""
    return '{"debug": true}'


@mcp.prompt()
async def review_code(code: str, language: str = "python") -> str:
    """Review a code snippet."""
    return f"Please review this {language} code:\n{code}"


if __name__ == "__main__":
    mcp.run()
