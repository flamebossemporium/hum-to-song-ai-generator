"""pyjnius binding to the JDK 21 formant shaper jar."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from hum2song.contracts.formant import FormantExtension

try:
    import jnius_config  # type: ignore

    _JAR = Path(__file__).parent / "target" / "hum2song-formant-0.2.1.jar"
    if _JAR.is_file():
        jnius_config.add_classpath(str(_JAR))
    from jnius import autoclass  # type: ignore
except ImportError:  # pragma: no cover
    autoclass = None


class JvmFormant:
    name = "jvm_formant"

    def __init__(self, options: dict) -> None:
        self.vowel = options.get("vowel", "ah")
        self.brightness = float(options.get