"""Bootstrap helper: install registry extensions into the local cache."""
from hum2song.host.registry import RegistryClient
from hum2song.utils.logging import get_logger

log = get_logger(__name__)


def main() -> int:
    client = RegistryClient.from_config()
    for ext in client.list_remote():
        log.info("installing %s (%s) v%s", ext.name, ext.language, ext.version)
        client.install(ext)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())