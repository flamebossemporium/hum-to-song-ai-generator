"""Formant contract: shape vowel character of a rendered voice."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class FormantExtension(Protocol):
    name: str

    def shape(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Return audio with formant envelope applied."""
        ...