from enum import Enum


class PluginStatus(Enum):
    OK = "ok"
    FAIL = "fail"
    WARNING = "warning"
    INFO = "info"
