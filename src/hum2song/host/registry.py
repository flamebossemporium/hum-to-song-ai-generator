"""Extension registry: tracks trusted extension names and versions."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import tomli

from hum2song.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class RegistryEntry:
    name: str
    version: str
    language: str
    sha256: str
    signed: bool


class ExtensionRegistry:
    """Reads config/registry.toml and answers trust questions."""

    def __init__(self, entries: dict[str, RegistryEntry]) -> None:
        self._entries = entries

    @classmethod
    def from_config(cls, host_cfg: dict) -> "ExtensionRegistry":
        manifest = Path(host_cfg["registry"]["manifest"])
        with manifest.open("rb") as fh:
            reg = tomli.load(fh)
        entries = {
            e["name"]: RegistryEntry(
                name=e["name"],
                version=e["version"],
                language=e["language"],
                sha256=e["sha256"],
                signed=e["signed"],
            )
            for e in reg["registry"]["extension"]
        }
        return cls(entries)

    def is_trusted(self, name: str) -> bool:
        entry = self._entries.get(name)
        return entry is not None and entry.signed

    def verify_digest(self, name: str, path: Path) -> bool:
        entry = self._entries.get(name)
        if entry is None:
            return False
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return digest == entry.sha256