# johan/commands/hej.py
from typing import Sequence, Any

from contracts.plugin_contract import IPluginCommand


class hej(IPluginCommand):
    def run(self, params: Sequence[str]) -> Any:
        print("Hej!", params if params else "")

    def help_short(self) -> str:
        return "Hälsar på dig."

    def help_long(self) -> str:
        return "Skriver ut en hälsning. Användning: hej [namn]"
