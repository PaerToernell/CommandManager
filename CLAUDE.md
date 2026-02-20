# CLAUDE.md - CommandManager

> Cross-project conventions: `F:\MyDev\strategy-generic\CLAUDE.md` (auto-loaded via `F:\MyDev\CLAUDE.md`).
> Current tasks and session log: `ROADMAP.md` (this repo).

## Vision

CommandManager is a dynamic, plugin-based CLI and REPL tool. Users invoke named plugin sets
(`ijob`, `docman`, `johan`...) and run commands within them. Commands are discovered at runtime
from the filesystem — no registration, no config files, no restarts needed.

## Design Goals (Non-Negotiable)

### 1. Loose Coupling
- The core (registry, dispatcher, REPL) knows nothing about specific plugins
- Plugins know nothing about each other
- The only contract between core and plugins is `IPluginCommand`
- Changes to a plugin never affect the core or other plugins

### 2. High Modularity
- Each command is a self-contained Python file
- Each plugin is a self-contained directory
- Core components (registry, dispatcher, service, REPL) are independent of each other

### 3. Separation of Concerns
- Discovery: `Registry` (finds and indexes commands)
- Resolution: `Dispatcher` (matches input to command)
- Execution: `PluginService` (runs command, captures result)
- Interaction: `repl.py` / entry points (user interface only)

### 4. Multi-Language Support
- Swedish å/ä/ö are distinct letters, not accent variants
- Help text, prompts, and output can be in any language
- System messages (REPL prompts, errors) should be localizable - not hardcoded English strings
- Language is a property of content, not tied to system locale

### 5. Cross-Platform
- No `.bat` files as entry points — use Python entry points via `pyproject.toml`
- No Windows-only paths or assumptions
- Works on Windows, macOS, Linux

## Architecture

### Plugin System Core
```
Registry        — discovers and indexes plugins from filesystem (singleton)
Dispatcher      — resolves input using longest-match-first algorithm
PluginRow       — lazy-loads a command file via importlib on first use
PluginService   — executes commands, captures output, returns PluginResult
IPluginCommand  — the only contract between core and plugins (ABC)
```

### Plugin Structure
```
commandmanager_plugins/
  contracts/
    plugin_contract.py          ← IPluginCommand ABC (run, help_short, help_long)
  plugins/
    <plugin_name>/
      commands/
        command_name.py         ← class command_name(IPluginCommand)
        multi_word_command.py   ← class multi_word_command (invoked as "multi word command")
        _private_helper.py      ← NOT registered (underscore prefix = private)
```

### Command Naming Convention
- Filename stem = class name = command name (with underscores replaced by spaces)
- `show.py` → `class show` → command `"show"`
- `command_create.py` → `class command_create` → command `"command create"`
- Class name MUST match file stem exactly (enforced at load time)
- Files starting with `_` are skipped by the registry

### Entry Points (Cross-Platform)
```toml
[project.scripts]
ijob   = "commandmanager.cli:run_ijob"
docman = "commandmanager.cli:run_docman"
```
After `pip install -e .`, these work on all platforms — no .bat files needed.

### Execution Flow
```
entry point (ijob, docman...)
  → bootstrap: identify plugin name, add commandmanager_plugins/ to sys.path
  → Registry.build_all(): discover all plugins (lazy — no modules loaded yet)
  → if CLI params: PluginService.execute() → Dispatcher → PluginRow.get_instance() → command.run()
  → if no params: REPL loop
```

### sys.path (Deliberate Design — Do NOT Change Without Discussion)
The `commandmanager_plugins/` directory is added to `sys.path` at startup. This allows plugins
to use short import paths:
```python
# CORRECT:
from contracts.plugin_contract import IPluginCommand

# WRONG (do not "fix" to this):
from commandmanager_plugins.contracts.plugin_contract import IPluginCommand
```

## Tech Stack

- **Python 3.11** — strict requirement
- **Pydantic v2** — for `PluginRow` and `PluginResult` models
- **pyproject.toml** — packaging and entry points (no .bat files)
- **prompt-toolkit** — planned for REPL enhancements
- **mypy / ruff / black / pytest** — dev tooling

## Files to Copy from Legacy Project

Core worth keeping (from `F:\MyDev\Legacy\CommandManagerOLD\src\commandmanager\`):
- `registry.py` — solid, copy as-is
- `dispatcher.py` — solid, copy as-is
- `plugin_object.py` — solid, copy as-is
- `plugin_service.py` — solid, copy as-is
- `plugin_result.py` — solid, copy as-is
- `plugin_status.py` — solid, copy as-is
- `repl.py` — copy, remove PyCharm stdin workaround (replace with prompt-toolkit)
- `help.py` — copy as-is
- `common/command_result_level.py` — copy as-is
- `AppData/.../contracts/plugin_contract.py` — copy as-is

Rebuild from scratch:
- Entry points (replace .bat files with `pyproject.toml` scripts)
- `bootstrap.py` / `setup.py` — rename and clean up sys.path logic
- `pyproject.toml` — clean, no exact `==` pins except where truly necessary

## Development Commands
```bash
# Install in editable mode (also installs entry point scripts)
pip install -e .

# Type checking
mypy src/

# Linting
ruff check src/

# Formatting
black src/

# Tests
pytest
```

## Development Rules
1. **Python 3.11 strict**
2. **Ask before changing sys.path logic**
3. **Ask before changing plugin import paths**
4. **Commands use `print()` for output** — captured by `redirect_stdout` in PluginService
5. **No platform-specific code in core** — entry points handle platform differences
6. **Language**: English in code, Swedish/English in comments and help text
