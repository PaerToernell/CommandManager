from abc import ABC, abstractmethod
from typing import Any

# Pattern imports (do not delete)
# from typing import Sequence, Any
# from contracts.plugin_contract import IPluginCommand


class IPluginCommand(ABC):
    """Defines the interface all plugin commands must implement."""

    @abstractmethod
    def run(self, params: tuple[str, ...] | None) -> Any:
        """Execute the command. May receive a tuple of string parameters or None."""
        pass

    @abstractmethod
    def help_short(self) -> str:
        """Return a short description of the command."""
        pass

    @abstractmethod
    def help_long(self) -> str:
        """Return a detailed description of the command."""
        pass
