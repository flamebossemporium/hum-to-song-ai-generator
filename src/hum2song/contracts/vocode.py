"""Vocode contract: turn pitch + envelope into a sung voice."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class VocodeExtension(Protocol):
    name: str

    def render(
        self,
        f0_hz: np.ndarray,
        envelope: np.ndarray,
        sample_rate: int,
    ) -> np.ndarray:
        """Return mono float32 waveform at sample_rate."""
        ...