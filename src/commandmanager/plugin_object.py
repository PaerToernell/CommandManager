from pathlib import Path
import importlib.util
from pydantic import BaseModel, Field


class PluginRow(BaseModel):
    path: Path                                         # obligatorisk input
    cache_instance: bool = False                       # kan sättas vid init
    name: str = Field(default="", init=False)          # beräknas internt, synligt utåt
    size: int = Field(default=0, init=False)           # beräknas internt, synligt utåt
    _instance: object | None = None                    # helt internt

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "from_attributes": True,
    }

    def model_post_init(self, __context):
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        self.name = self.path.name
        self.size = self.path.stat().st_size

    def get_instance(self):
        if self.cache_instance and self._instance is not None:
            return self._instance

        spec = importlib.util.spec_from_file_location(self.path.stem, self.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cls_name = self.path.stem
        if not hasattr(module, cls_name):
            raise RuntimeError(f"Command file '{self.name}' must define class '{cls_name}'.")

        cls = getattr(module, cls_name)
        instance = cls()

        if not hasattr(instance, "run"):
            raise RuntimeError(f"Class '{cls_name}' in '{self.name}' has no 'run()' method.")

        if self.cache_instance:
            self._instance = instance
        return instance

    def __repr__(self):
        return f"<FileObject {self.name} ({self.size} bytes)>"
