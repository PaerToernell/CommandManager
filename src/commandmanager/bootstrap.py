import sys
from pathlib import Path

from .registry import Registry
from .plugin_service import PluginService


def setup(plugin_name: str) -> PluginService:
    """Locate commandmanager_plugins/, add to sys.path, build registry, return PluginService."""
    plugins_root = _find_plugins_root()

    # Add to sys.path so plugins can use short imports (e.g. from contracts.plugin_contract import IPluginCommand)
    plugins_root_str = str(plugins_root)
    if plugins_root_str not in sys.path:
        sys.path.insert(0, plugins_root_str)

    plugins_dir = plugins_root / "plugins"

    registry = Registry.instance()
    registry.build_all(plugins_dir, default_plugin=plugin_name)

    return PluginService(registry)


def _find_plugins_root() -> Path:
    """Find the commandmanager_plugins/ directory."""
    # Relative to this package: src/commandmanager/ -> src/ -> project root
    package_dir = Path(__file__).parent
    candidate = package_dir.parent.parent / "commandmanager_plugins"
    if candidate.exists():
        return candidate

    # Fallback: relative to current working directory
    cwd_candidate = Path.cwd() / "commandmanager_plugins"
    if cwd_candidate.exists():
        return cwd_candidate

    raise FileNotFoundError(
        f"commandmanager_plugins/ not found. Tried:\n"
        f"  {candidate}\n"
        f"  {cwd_candidate}"
    )
