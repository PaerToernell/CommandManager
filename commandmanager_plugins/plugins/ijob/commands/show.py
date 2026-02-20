# ijob/commands/show.py
from typing import Sequence, Any

from contracts.plugin_contract import IPluginCommand


class show(IPluginCommand):
    def run(self, params: Sequence[str]) -> Any:
        print("No action implemented for `show` command.")

    def help_short(self) -> str:
        return "show: brief help"

    def help_long(self) -> str:
        return "show: long help"
