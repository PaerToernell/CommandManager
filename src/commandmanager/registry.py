from pathlib import Path

from .plugin_object import PluginRow


class Registry:
    _instance = None  # singleton storage

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, debug=False):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._plugins: dict[str, dict[str, PluginRow]] = {}
        self._current_plugin: str | None = None
        self._debug = debug
        self._initialized = True

    def build(self, commands_path):
        """Build exactly one plugin and make it default (back-compat)."""
        path = Path(commands_path)
        if not path.exists():
            raise FileNotFoundError(f"Commands folder not found: {path}")
        plugin_name = path.parent.name
        self._build_plugin(plugin_name, path)
        self._current_plugin = plugin_name
        if self._debug:
            print(f"[BUILT] plugin '{plugin_name}' with {len(self._plugins[plugin_name])} commands")

    def build_all(self, plugins_root, default_plugin: str | None = None):
        """Auto-discover all plugins from plugins_root/."""
        root = Path(plugins_root)
        if not root.exists():
            raise FileNotFoundError(f"Plugins root not found: {root}")

        for plugin_dir in root.iterdir():
            cmd_path = plugin_dir / "commands"
            if cmd_path.is_dir():
                self._build_plugin(plugin_dir.name, cmd_path)

        if default_plugin and default_plugin in self._plugins:
            self._current_plugin = default_plugin
        elif not self._current_plugin and self._plugins:
            self._current_plugin = next(iter(self._plugins))

        if self._debug:
            print(f"[BUILT ALL] Loaded {len(self._plugins)} plugins from {root}, default={self._current_plugin}")

    def _build_plugin(self, plugin_name, path: Path):
        items: dict[str, PluginRow] = {}
        for f in Path(path).rglob("*.py"):
            if f.name == "__init__.py" or f.name.startswith("_"):
                continue
            cmd_name = f.stem.replace("_", " ")
            fo = PluginRow(path=f)
            items[cmd_name] = fo
            if self._debug:
                self._debug_command(plugin_name, cmd_name, fo)
        self._plugins[plugin_name] = items

    def _debug_command(self, plugin_name, cmd_name, fo: PluginRow):
        try:
            instance = fo.get_instance()
            has_run = hasattr(instance, "run")
        except Exception as e:
            has_run = False
            print(f"[ERROR] {fo.path}: {e}")
        print(f"[{plugin_name}] {cmd_name:25s} -> {fo.path.name:20s} | run() = {has_run}")

    def getObj(self, cmd_name, plugin_name=None):
        if plugin_name:
            return self._plugins.get(plugin_name, {}).get(cmd_name)
        if self._current_plugin:
            return self._plugins.get(self._current_plugin, {}).get(cmd_name)
        return None

    def list_this(self):
        return self._plugins.get(self._current_plugin, {})

    def list_plugin(self, plugin_name):
        return self._plugins.get(plugin_name, {})

    def list_all(self):
        combined = {}
        for pname, items in self._plugins.items():
            for cmd_name, fo in items.items():
                combined[f"{pname}:{cmd_name}"] = fo
        return combined

    def all_plugins(self):
        return list(self._plugins.keys())

    def current_plugin(self):
        return self._current_plugin

    def set_current_plugin(self, name):
        if name in self._plugins:
            self._current_plugin = name
        else:
            raise ValueError(f"Plugin not found: {name}")
