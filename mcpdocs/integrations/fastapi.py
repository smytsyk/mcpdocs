import asyncio
import logging
import threading
from pathlib import Path

from mcpdocs.generator import McpDocs

logger = logging.getLogger("mcpdocs")

_DEFAULT_OUTPUT_DIR = ".mcpdocs-static"
_DEFAULT_MOUNT_PATH = "/mcpdocs"


def setup_mcpdocs(
    app: object,
    url: str,
    output_dir: str | None = None,
    mount_path: str = _DEFAULT_MOUNT_PATH,
    timeout: float = 30.0,
    auto_regenerate: bool = True,
) -> None:
    """
    Mount auto-generated MCP documentation on a FastAPI app.

    Args:
        app: FastAPI application instance.
        url: SSE URL of the running MCP server.
        output_dir: Directory for generated static files. Defaults to ".mcpdocs-static".
        mount_path: URL path to mount docs at. Defaults to "/mcpdocs".
        timeout: Timeout in seconds for MCP introspection. Defaults to 30.
        auto_regenerate: Regenerate docs on setup. Defaults to True.

    """
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse
    from starlette.staticfiles import StaticFiles

    if not isinstance(app, FastAPI):
        msg = f"Expected FastAPI instance, got {type(app).__name__}"
        raise TypeError(msg)

    static_dir = Path(output_dir or _DEFAULT_OUTPUT_DIR).resolve()

    if auto_regenerate:
        _regenerate(url, str(static_dir), timeout)

    if not static_dir.is_dir():
        logger.warning(
            "mcpdocs static directory not found at %s, skipping mount", static_dir
        )
        return

    bare_path = mount_path.rstrip("/")

    @app.get(bare_path, include_in_schema=False)
    async def mcpdocs_redirect() -> RedirectResponse:
        return RedirectResponse(url=f"{bare_path}/")

    app.mount(
        bare_path,
        StaticFiles(directory=str(static_dir), html=True),
        name="mcpdocs",
    )

    logger.info("mcpdocs mounted at %s", bare_path)


def _regenerate(
    url: str,
    output_dir: str,
    timeout: float,
) -> bool:
    try:
        docs = McpDocs(url=url, timeout=timeout)
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():

                def _run() -> None:
                    asyncio.run(docs.generate(output_dir))

                t = threading.Thread(target=_run)
                t.start()
                t.join()
            else:
                asyncio.run(docs.generate(output_dir))
        except RuntimeError:
            # No running loop
            asyncio.run(docs.generate(output_dir))

        logger.info("mcpdocs regenerated at %s", output_dir)
        return True
    except Exception:
        logger.warning("mcpdocs generation failed", exc_info=True)
    return False
