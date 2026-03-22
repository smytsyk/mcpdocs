# Changelog

## 0.1.0 - 2026-03-22

Initial release.

- CLI: `mcpdocs generate` and `mcpdocs inspect` commands
- SSE transport: connects to any running MCP server via SSE URL
- Introspects tools, resources, resource templates, and prompts
- Generates static HTML documentation with cyberpunk theme
- FastAPI integration: `setup_mcpdocs(app, url=...)` with auto-regeneration
- Light/dark mode with OS preference detection
- Search/filter on all catalog pages
- Collapsible JSON Schema sections for tool parameters
