from datetime import UTC, datetime
from urllib.parse import urlparse

import mcp.types as types
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

from mcpdocs._version import __version__
from mcpdocs.exceptions import IntrospectionError
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

_ALLOWED_SCHEMES = {"http", "https"}
_MAX_PAGES = 100


class Introspector:
    def __init__(
        self,
        url: str,
        timeout: float = 30.0,
    ) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in _ALLOWED_SCHEMES:
            raise IntrospectionError(
                f"URL must use http:// or https://, got: {parsed.scheme or 'none'}://"
            )
        self._url = url
        self._timeout = timeout

    async def introspect(self) -> ServerSpec:
        try:
            async with sse_client(self._url) as (read_stream, write_stream):
                async with ClientSession(
                    read_stream,
                    write_stream,
                    client_info=types.Implementation(
                        name="mcpdocs", version=__version__
                    ),
                ) as session:
                    return await self._collect(session)
        except Exception as e:
            raise IntrospectionError(
                f"Failed to connect to MCP server at {self._url}: {e}"
            ) from e

    async def _collect(self, session: ClientSession) -> ServerSpec:
        try:
            init_result = await session.initialize()
        except Exception as e:
            raise IntrospectionError(f"MCP initialize failed: {e}") from e

        server_info = self._extract_server_info(init_result)
        capabilities = self._extract_capabilities(init_result)

        tools: list[ToolSpec] = []
        resources: list[ResourceSpec] = []
        resource_templates: list[ResourceTemplateSpec] = []
        prompts: list[PromptSpec] = []

        if capabilities.tools:
            tools = await self._list_tools(session)

        if capabilities.resources:
            resources = await self._list_resources(session)
            resource_templates = await self._list_resource_templates(session)

        if capabilities.prompts:
            prompts = await self._list_prompts(session)

        return ServerSpec(
            server_info=server_info,
            capabilities=capabilities,
            tools=tools,
            resources=resources,
            resource_templates=resource_templates,
            prompts=prompts,
            generated_at=datetime.now(UTC),
        )

    @staticmethod
    def _extract_server_info(init_result: types.InitializeResult) -> ServerInfo:
        return ServerInfo(
            name=init_result.serverInfo.name,
            version=getattr(init_result.serverInfo, "version", None),
            protocol_version=str(init_result.protocolVersion),
        )

    @staticmethod
    def _extract_capabilities(
        init_result: types.InitializeResult,
    ) -> ServerCapabilities:
        caps = init_result.capabilities
        return ServerCapabilities(
            tools=caps.tools is not None,
            resources=caps.resources is not None,
            prompts=caps.prompts is not None,
            logging=caps.logging is not None if hasattr(caps, "logging") else False,
            subscriptions=False,
        )

    async def _list_tools(self, session: ClientSession) -> list[ToolSpec]:
        items: list[ToolSpec] = []
        cursor = None
        for _ in range(_MAX_PAGES):
            try:
                if cursor:
                    result = await session.list_tools(
                        params=types.PaginatedRequestParams(cursor=cursor),
                    )
                else:
                    result = await session.list_tools()
            except Exception as e:
                raise IntrospectionError(f"tools/list failed: {e}") from e

            for tool in result.tools:
                annotations = None
                if tool.annotations:
                    annotations = ToolAnnotations(
                        read_only=getattr(tool.annotations, "readOnlyHint", None),
                        destructive=getattr(tool.annotations, "destructiveHint", None),
                        idempotent=getattr(tool.annotations, "idempotentHint", None),
                        open_world=getattr(tool.annotations, "openWorldHint", None),
                    )
                items.append(
                    ToolSpec(
                        name=tool.name,
                        description=tool.description,
                        input_schema=tool.inputSchema,
                        annotations=annotations,
                    )
                )
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return items

    async def _list_resources(self, session: ClientSession) -> list[ResourceSpec]:
        items: list[ResourceSpec] = []
        cursor = None
        for _ in range(_MAX_PAGES):
            try:
                if cursor:
                    result = await session.list_resources(
                        params=types.PaginatedRequestParams(cursor=cursor),
                    )
                else:
                    result = await session.list_resources()
            except Exception as e:
                raise IntrospectionError(f"resources/list failed: {e}") from e

            for resource in result.resources:
                items.append(
                    ResourceSpec(
                        uri=str(resource.uri),
                        name=resource.name,
                        description=resource.description,
                        mime_type=resource.mimeType,
                    )
                )
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return items

    async def _list_resource_templates(
        self, session: ClientSession
    ) -> list[ResourceTemplateSpec]:
        items: list[ResourceTemplateSpec] = []
        cursor = None
        for _ in range(_MAX_PAGES):
            try:
                if cursor:
                    result = await session.list_resource_templates(
                        params=types.PaginatedRequestParams(cursor=cursor),
                    )
                else:
                    result = await session.list_resource_templates()
            except Exception as e:
                raise IntrospectionError(f"resources/templates/list failed: {e}") from e

            for template in result.resourceTemplates:
                items.append(
                    ResourceTemplateSpec(
                        uri_template=str(template.uriTemplate),
                        name=template.name,
                        description=template.description,
                        mime_type=template.mimeType,
                    )
                )
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return items

    async def _list_prompts(self, session: ClientSession) -> list[PromptSpec]:
        items: list[PromptSpec] = []
        cursor = None
        for _ in range(_MAX_PAGES):
            try:
                if cursor:
                    result = await session.list_prompts(
                        params=types.PaginatedRequestParams(cursor=cursor),
                    )
                else:
                    result = await session.list_prompts()
            except Exception as e:
                raise IntrospectionError(f"prompts/list failed: {e}") from e

            for prompt in result.prompts:
                arguments = []
                if prompt.arguments:
                    for arg in prompt.arguments:
                        arguments.append(
                            PromptArgument(
                                name=arg.name,
                                description=arg.description,
                                required=arg.required or False,
                            )
                        )
                items.append(
                    PromptSpec(
                        name=prompt.name,
                        description=prompt.description,
                        arguments=arguments,
                    )
                )
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return items
