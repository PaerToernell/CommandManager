import shlex

from prompt_toolkit import PromptSession


def run_repl(service, plugin_name: str) -> None:
    """Run the REPL loop using prompt-toolkit for input."""
    print("Entering REPL mode. Type 'exit' to quit.\n")
    session = PromptSession()

    while True:
        try:
            line = session.prompt(f"{plugin_name}> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not line:
            continue
        if line.lower() in ("exit", "quit"):
            print("Bye.")
            break

        try:
            cmd_parts = shlex.split(line)
        except ValueError as e:
            print(f"Input error: {e}")
            continue

        result = service.execute(cmd_parts)
        service.print_result(result)
