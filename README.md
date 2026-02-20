# CommandManager

A dynamic, plugin-based CLI and REPL tool. Commands are discovered at runtime from the filesystem — no registration, no config files, no restarts needed.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# Enter REPL for a plugin
ijob

# Run a command directly
ijob show

# Other plugins
johan
```

## Plugin Structure

```
commandmanager_plugins/
  contracts/
    plugin_contract.py     ← IPluginCommand ABC
  plugins/
    <plugin_name>/
      commands/
        command_name.py    ← class command_name(IPluginCommand)
```

## Dev

```bash
mypy src/
ruff check src/
black src/
pytest
```
