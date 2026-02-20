import sys

from . import bootstrap
from .repl import run_repl


def run_ijob():
    _run("ijob")


def run_docman():
    _run("docman")


def run_johan():
    _run("johan")


def _run(plugin_name: str):
    service = bootstrap.setup(plugin_name)
    params = sys.argv[1:]
    if params:
        result = service.execute(params)
        service.print_result(result)
    else:
        run_repl(service, plugin_name)
