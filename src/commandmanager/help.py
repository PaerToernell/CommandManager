from typing import List

HELP_FLAGS = {"-h", "--help", "help"}


class Help:
    def __init__(self) -> None:
        pass

    def run(self, parts: List[str]) -> None:
        if not parts or (len(parts) == 1 and parts[0] in HELP_FLAGS):
            self._print_general_help()
            return

        cmd_name = parts[0]
        if len(parts) > 1 and any(p in HELP_FLAGS for p in parts[1:]):
            self._print_command_help(cmd_name)
            return

        self._print_command_help(cmd_name)

    def _print_general_help(self) -> None:
        print("Usage: <command> [args]")
        print("Global flags: -h, --help, help")
        print("Use '<command> -h' to get help for a specific command.")

    def _print_command_help(self, command_name: str) -> None:
        print(f"Help for command: {command_name}")
        print("No detailed help available (stub).")
