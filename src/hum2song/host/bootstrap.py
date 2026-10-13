"""Host bootstrap: read config, build loader, register extensions."""
from __future__ import annotations

import tomli
from pathlib import Path

from hum2song.host.loader import ExtensionLoader
from hum2song.host.registry import ExtensionRegistry
from hum2song.utils.logging import get_logger

log = get_logger(__name__)
CONFIG_PATH = Path("config/host.toml")


def bootstrap(config_path: Path = CONFIG_PATH) -> ExtensionLoader:
    """Load host.toml, build the loader, discover and register extensions."""
    with config_path.open("rb") as fh:
        cfg = tomli.load(fh)

    registry = ExtensionRegistry.from_config(cfg)
    loader = ExtensionLoader(
        search_paths=[Path(p).expanduser() for p in cfg["paths"]["extension_search"]],
        registry=registry,
        strict=cfg["loader"]["strict_contract"],
    )

    for name in cfg["loader"]["enabled"]:
        try:
            loader.load(name)
        except FileNotFoundError:
            log.warning("extension %s not found, skipping", name)

    log.info("host ready: %d extensions loaded", len(loader.loaded))
    return loader