import asyncio
import json
from typing import Annotated

import typer

from mcpdocs.exceptions import IntrospectionError, RenderError
from mcpdocs.generator import McpDocs

app = typer.Typer(
    name="mcpdocs",
    help="Static documentation generator for MCP servers.",
    no_args_is_help=True,
)


@app.command()
def generate(
    url: Annotated[str, typer.Option("--url", "-u", help="SSE URL of the MCP server")],
    output: Annotated[
        str, typer.Option("--output", "-o", help="Output directory")
    ] = "./site",
    timeout: Annotated[
        float, typer.Option("--timeout", "-t", help="Timeout per call in seconds")
    ] = 30.0,
) -> None:
    """Introspect an MCP server and generate static HTML documentation."""
    docs = McpDocs(url=url, timeout=timeout)
    try:
        spec = asyncio.run(docs.generate(output))
        tools_n = len(spec.tools)
        resources_n = len(spec.resources)
        prompts_n = len(spec.prompts)
        typer.echo(
            f"Documentation generated in {output}/ "
            f"({tools_n} tools, {resources_n} resources, {prompts_n} prompts)"
        )
    except IntrospectionError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    except RenderError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=3)


@app.command()
def inspect(
    url: Annotated[str, typer.Option("--url", "-u", help="SSE URL of the MCP server")],
    timeout: Annotated[
        float, typer.Option("--timeout", "-t", help="Timeout per call in seconds")
    ] = 30.0,
) -> None:
    """Introspect an MCP server and dump the spec as JSON."""
    docs = McpDocs(url=url, timeout=timeout)
    try:
        spec = asyncio.run(docs.introspect())
        typer.echo(json.dumps(spec.model_dump(mode="json"), indent=2))
    except IntrospectionError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
