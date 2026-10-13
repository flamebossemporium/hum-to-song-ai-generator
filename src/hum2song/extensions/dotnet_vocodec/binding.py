"""pythonnet binding to the .NET 8 vocoder assembly."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from hum2song.contracts.vocode import VocodeExtension

try:
    import clr  # type: ignore
except ImportError:  # pragma: no cover
    clr = None

_ASSEMBLY = Path(__file__).parent / "bin" / "Release" / "net8.0" / "Hum2Song.Vocodec.dll"


class DotnetVocodec:
    name = "dotnet_vocodec"

    def __init__(self, options: dict) -> None:
        self.breathiness = float(options.get("breathiness", 0.15))
        self.vibrato_hz = float(options.get("vibrato_hz", 5.2))
        self._impl = None
        if clr is not None and _ASSEMBLY.is_file():
            clr.AddReference(str(_ASSEMBLY))
            from Hum2Song.Vocodec import Renderer  # type: ignore

            self._impl = Renderer(self.breathiness, self.vibrato_hz)

    def render(
        self,
        f0_hz: np.ndarray,
        envelope: np.ndarray,
        sample_rate: int,
    ) -> np.ndarray:
        if self._impl is None:
            return self._fallback(f0_hz, envelope, sample_rate)
        out = self._impl.Render(
            f0_hz.tolist(), envelope.tolist(), sample_rate
        )
        return np.asarray(out, dtype=np.float32)

    def _fallback(self, f0_hz, envelope, sample_rate):
        # Simple sine + breath noise so the pipeline still runs without .NET.
        t = np.arange(len(f0_hz), dtype=np.float32) / sample_rate
        phase = 2.0 * np.pi * np.cumsum(f0_hz) / sample_rate
        tone = np.sin(phase).astype(np.float32)
        noise = np.random.default_rng(0).normal(0, self.breathiness, len(tone))
        return ((tone + noise.astype(np.float32)) * envelope).astype(np.float32)


def build(options: dict) -> DotnetVocodec:
    return DotnetVocodec(options)