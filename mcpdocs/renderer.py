import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from mcpdocs._version import __version__
from mcpdocs.exceptions import RenderError
from mcpdocs.models import ServerSpec

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_PAGES = ["resources.html", "prompts.html"]


class Renderer:
    def __init__(self) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(_TEMPLATES_DIR)),
            autoescape=True,
        )

    def render(self, spec: ServerSpec, output_dir: str) -> None:
        try:
            os.makedirs(output_dir, exist_ok=True)
            context = self._build_context(spec)
            self._render_page(
                "tools.html", context, output_dir, output_name="index.html"
            )
            for page in _PAGES:
                self._render_page(page, context, output_dir)
            self._copy_static(output_dir)
        except Exception as e:
            if isinstance(e, RenderError):
                raise
            raise RenderError(f"Rendering failed: {e}") from e

    def _build_context(self, spec: ServerSpec) -> dict[str, object]:
        return {
            "server_name": spec.server_info.name,
            "server_version": spec.server_info.version,
            "protocol_version": spec.server_info.protocol_version,
            "capabilities": spec.capabilities,
            "tools": spec.tools,
            "resources": spec.resources,
            "resource_templates": spec.resource_templates,
            "prompts": spec.prompts,
            "tools_count": len(spec.tools),
            "resources_count": len(spec.resources) + len(spec.resource_templates),
            "prompts_count": len(spec.prompts),
            "mcpdocs_version": __version__,
            "generated_at": spec.generated_at.strftime("%Y-%m-%d %H:%M UTC"),
        }

    def _render_page(
        self,
        template_name: str,
        context: dict[str, object],
        output_dir: str,
        output_name: str | None = None,
    ) -> None:
        active_page = template_name.replace(".html", "")
        template = self._env.get_template(template_name)
        html = template.render(**context, active_page=active_page)
        output_path = os.path.join(output_dir, output_name or template_name)
        with open(output_path, "w") as f:
            f.write(html)

    @staticmethod
    def _copy_static(output_dir: str) -> None:
        src = _TEMPLATES_DIR / "static"
        dst = os.path.join(output_dir, "static")
        if src.is_dir():
            shutil.copytree(str(src), dst, dirs_exist_ok=True)
