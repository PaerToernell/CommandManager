from contextlib import redirect_stdout
import io
import traceback
from typing import List

from .dispatcher import Dispatcher
from .registry import Registry
from .common.command_result_level import CommandResultLevel
from .plugin_result import PluginResult


class PluginService:
    """
    Service layer for command execution that returns PluginResult.
    Captures printed output using redirect_stdout and includes tracebacks on exceptions.
    """

    def __init__(self, registry: Registry, result_view: CommandResultLevel = CommandResultLevel.NORMAL):
        self.registry = registry
        self.dispatcher = Dispatcher(self.registry)
        self.result_view = result_view

    def execute(self, cli_params: List[str]) -> PluginResult:
        if not cli_params:
            return PluginResult.fail(message="Empty command", error_code=1)

        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                self.dispatcher.run(cli_params)
            output = buf.getvalue()
            return PluginResult.ok(output=output, message=None)
        except Exception as exc:
            tb = traceback.format_exc()
            return PluginResult.fail(message=str(exc), error_code=1, output=buf.getvalue(), traceback=tb)

    def print_result(self, result: PluginResult):
        if self.result_view == CommandResultLevel.NORMAL:
            if result.output and result.output.strip():
                print(result.output.strip())
            elif result.message:
                print(result.message)
            return

        if self.result_view == CommandResultLevel.ALL:
            print(result.model_dump_json(indent=2, exclude_none=True))
