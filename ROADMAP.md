# CommandManager Roadmap

> Tasks and session log. See `CLAUDE.md` for architecture.

## Current Focus

### Core
- [ ] Help system — wire dispatcher help into actual command help_short/help_long output
- [ ] Command not found — better error message (list available commands?)
- [ ] REPL history — prompt-toolkit history file

### Plugins
- [ ] Add more ijob commands (from legacy or new)
- [ ] docman plugin — placeholder commands

### Packaging
- [ ] .gitignore for `commandmanager_plugins/` AppData (user-local plugins)
- [ ] Consider plugin discovery from user AppData (cross-platform path)

## Completed

### 2026-02-20 (session 2) — Strategy restructure
- Created strategy-commandmanager repo (now superseded — ROADMAP moved here)
- Fixed stale reference in CLAUDE.md (docman-strategy → strategy-generic + strategy-commandmanager)

### 2026-02-20 — Initial project setup
- New repo created (PaerToernell/CommandManager), fresh start replacing archived old project
- pyproject.toml with entry points (ijob, docman, johan) — cross-platform, no .bat files
- src layout with full core: registry, dispatcher, plugin_object, plugin_service,
  plugin_result, plugin_status, help, bootstrap, cli
- repl.py rebuilt with prompt-toolkit PromptSession (removed PyCharm stdin hack)
- All imports fixed to relative — no sys.path hacks in core
- commandmanager_plugins/ with contracts/plugin_contract.py and example plugins
  (ijob/show, johan/hej)
- Verified: `pip install -e .`, `ijob show`, `johan hej` all work
