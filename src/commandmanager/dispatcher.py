import traceback

from .help import Help


class Dispatcher:
    HELP_FLAGS = {"-h", "--help", "help"}

    def __init__(self, registry):
        self.registry = registry
        self.help_runner = Help()

    def run(self, parts: list[str]):
        if not parts:
            return

        # Global help (only when single token)
        if len(parts) == 1 and parts[0] in self.HELP_FLAGS:
            self.help_runner.run(parts)
            return

        # Find longest matching command
        for i in range(len(parts), 0, -1):
            cmd_name = " ".join(parts[:i])
            try:
                cmd_obj = self.registry.getObj(cmd_name)
            except Exception as e:
                print(f"Dispatcher: registry.getObj raised: {e}")
                return

            if cmd_obj:
                params = parts[i:]
                if params and params[-1] in self.HELP_FLAGS:
                    full_params = [cmd_name] + params
                    self.help_runner.run(full_params)
                else:
                    self._execute(cmd_obj, params)
                return

        print(f"Dispatcher: Unknown command: {parts[0]}")

    def _execute(self, cmd_obj, params: list[str]):
        try:
            target = cmd_obj.get_instance()
        except Exception as e:
            print(f"Dispatcher: failed to get instance from command object: {e}")
            traceback.print_exc()
            return

        instance = target
        if callable(target) and not hasattr(target, "run"):
            try:
                instance = target()
            except Exception:
                instance = target

        if hasattr(instance, "run"):
            try:
                instance.run(params)
            except StopIteration as e:
                print(f"Dispatcher: command run() raised StopIteration: {e}")
                raise
        else:
            print(f"Command '{cmd_obj}' has no 'run' method.")
