# mcpdocs

**Static documentation generator for MCP servers — like Swagger UI, but for MCP.**

`mcpdocs` introspects running Model Context Protocol (MCP) servers via SSE and generates a beautiful, searchable static documentation site. It helps developers and users understand the tools, resources, and prompts available in an MCP server.

## Features

- 🔍 **Auto-Introspection**: Connects to any running MCP server via SSE URL to discover its capabilities.
- 🛠️ **Full Support**: Documents Tools, Resources, Resource Templates, and Prompts.
- 🎨 **Beautiful UI**: Clean, responsive, and searchable documentation with dark mode support.
- 🚀 **FastAPI Integration**: Easily mount auto-generated docs on your existing FastAPI application.
- 📦 **Static Output**: Generates pure HTML/CSS that can be hosted anywhere (GitHub Pages, S3, etc.).
- 🤖 **CI/CD Ready**: CLI-first design for automated documentation workflows.

## Installation

```bash
pip install mcpdocs
```

To use the FastAPI integration:

```bash
pip install "mcpdocs[fastapi]"
```

## Usage

### 1. Command Line Interface (CLI)

The CLI tool is named `mcpdocs`. To generate documentation, you provide the SSE URL of your running server.

**Basic Example:**
```bash
mcpdocs generate --url "http://localhost:8000/sse"
```

**Custom Output Directory:**
```bash
mcpdocs generate --url "http://localhost:8000/sse" --output "./static-docs"
```

#### CLI Reference

| Flag | Shortcut | Description |
|------|----------|-------------|
| `--url` | `-u` | **(Required)** The SSE URL of the running MCP server. |
| `--output` | `-o` | Where to save the HTML (default: `./site`). |
| `--timeout` | `-t` | Seconds to wait for server responses (default: `30.0`). |

---

### 2. FastAPI Integration

You can serve the documentation site directly from your FastAPI application.

```python
from fastapi import FastAPI
from mcpdocs.integrations.fastapi import setup_mcpdocs

app = FastAPI()

setup_mcpdocs(
    app,
    url="http://localhost:8000/sse",
    mount_path="/docs/mcp",
    output_dir=".mcpdocs-cache"
)
```

#### Python API Reference (`setup_mcpdocs`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `app` | `FastAPI` | Your FastAPI application instance. |
| `url` | `str` | The SSE URL of the running MCP server. |
| `mount_path` | `str` | URL path where docs will be served (default: `/mcpdocs`). |
| `output_dir` | `str` | Local path to store static files (default: `.mcpdocs-static`). |
| `timeout` | `float` | Seconds to wait for server responses (default: `30.0`). |
| `auto_regenerate`| `bool` | If `True`, regenerates docs on app startup (default: `True`). |

---

### 3. Inspect (JSON dump)

Dump the raw server spec as JSON — useful for CI or debugging:

```bash
mcpdocs inspect --url "http://localhost:8000/sse"
```

---

## How it works

1. **Introspection**: `mcpdocs` connects to the provided SSE URL.
2. **Connection**: It establishes a JSON-RPC connection over the SSE transport.
3. **Discovery**: It queries the server for all available tools, resources, and prompts.
4. **Rendering**: It generates a standalone static website using Jinja2 templates.

## Security

Only run `mcpdocs` against trusted MCP servers. The generated documentation does not include sensitive configuration details of the server.

## License

MIT
