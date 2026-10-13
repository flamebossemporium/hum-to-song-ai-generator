"""Extension loader: discovers manifests, imports modules, wires contracts."""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import tomli

from hum2song.contracts.pitch import PitchExtension
from hum2song.host.registry import ExtensionRegistry
from hum2song.utils.logging import get_logger

log = get_logger(__name__)


class ExtensionLoader:
    """Loads extension modules by name from configured search paths.

    Concurrency: not thread-safe. Build once on startup, then read-only.
    """

    def __init__(
        self,
        search_paths: list[Path],
        registry: ExtensionRegistry,
        strict: bool = True,
    ) -> None:
        self.search_paths = search_paths
        self.registry = registry
        self.strict = strict
        self.loaded: dict[str, Any] = {}

    def _find_manifest(self, name: str) -> Path:
        for root in self.search_paths:
            manifest = root / name / "extension.toml"
            if manifest.is_file():
                return manifest
        raise FileNotFoundError(f"no manifest for extension {name!r}")

    def load(self, name: str) -> Any:
        """Load one extension by name. Idempotent."""
        if name in self.loaded:
            return self.loaded[name]

        manifest_path = self._find_manifest(name)
        with manifest_path.open("rb") as fh:
            manifest = tomli.load(fh)

        if self.strict and not self.registry.is_trusted(manifest["extension"]["name"]):
            raise PermissionError(f"untrusted extension {name!r}")

        module_path = manifest["extension"]["entry_module"]
        module = importlib.import_module(module_path)
        instance = module.build(manifest["extension"].get("options", {}))

        if self.strict and not isinstance(instance, PitchExtension):
            raise TypeError(f"{name!r} does not satisfy PitchExtension")

        self.loaded[name] = instance
        log.debug("loaded extension %s from %s", name, module_path)
        return instance

    def get(self, name: str) -> Any:
        if name not in self.loaded:
            raise KeyError(f"extension {name!r} not loaded")
        return self.loaded[name]