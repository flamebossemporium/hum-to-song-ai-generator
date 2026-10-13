"""Pitch stage: delegate to the loaded pitch extension."""
from __future__ import annotations

import numpy as np

from hum2song.contracts.pitch import PitchResult
from hum2song.host.loader import ExtensionLoader


def run_pitch_stage(
    audio: np.ndarray,
    sample_rate: int,
    loader: ExtensionLoader,
    preferred: str = "native_pitch",
) -> PitchResult:
    """Run the preferred pitch extension, falling back to any loaded one."""
    try:
        ext = loader.get(preferred)
    except KeyError:
        if not loader.loaded:
            raise RuntimeError("no pitch extension loaded") from None
        ext = next(iter(loader.loaded.values()))
    return ext.extract(audio, sample_rate)