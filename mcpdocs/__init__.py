from mcpdocs._version import __version__
from mcpdocs.generator import McpDocs


def setup_mcpdocs(*args, **kwargs):
    """Convenience wrapper for the FastAPI integration."""
    try:
        from mcpdocs.integrations.fastapi import setup_mcpdocs as setup

        return setup(*args, **kwargs)
    except ImportError:
        raise ImportError(
            "FastAPI integration requires 'mcpdocs[fastapi]' to be installed."
        )


__all__ = ["McpDocs", "__version__", "setup_mcpdocs"]
