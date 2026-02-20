from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from .plugin_status import PluginStatus


class PluginResult(BaseModel):
    """Represents the result of a plugin execution."""

    success: bool
    error: Optional[str] = None
    status: PluginStatus = Field(default=PluginStatus.INFO)
    message: Optional[str] = None
    traceback: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    error_code: int = 0
    data: Optional[Any] = None
    output: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return bool(self.success)

    @classmethod
    def ok(cls, output: Optional[str] = None, message: Optional[str] = None, data: Optional[Any] = None) -> "PluginResult":
        return cls(
            success=True,
            error=None,
            status=PluginStatus.OK,
            message=message,
            output=output,
            data=data,
            error_code=0,
        )

    @classmethod
    def fail(cls, message: Optional[str] = None, error_code: int = 1, output: Optional[str] = None, traceback: Optional[str] = None, data: Optional[Any] = None) -> "PluginResult":
        return cls(
            success=False,
            error=message,
            status=PluginStatus.FAIL,
            message=message,
            output=output,
            traceback=traceback,
            error_code=error_code,
            data=data,
        )
