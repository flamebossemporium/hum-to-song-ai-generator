"""Tempo stage: estimate BPM and beat grid from the pitch contour."""
from __future__ import annotations

import numpy as np


def run_tempo_stage(f0_hz: np.ndarray, hop_ms: float) -> tuple[float, np.ndarray]:
    """Return (bpm, beat_times_seconds).

    Simple autocorrelation on the voiced-mask onset envelope. Good enough
    for humming; swap for librosa.beat.beat_track if you need accuracy.
    """
    voiced = ~np.isnan(f0_hz)
    onset = np.diff(voiced.astype(np.float32))
    onset[onset < 0] = 0.0
    if onset.sum() == 0:
        return 120.0, np.array([], dtype=np.float32)

    ac = np.correlate(onset, onset, mode="full")[len(onset) - 1 :]
    min_lag = int(0.3 / (hop_ms / 1000.0))
    max_lag = int(1.2 / (hop_ms / 1000.0))
    peak = min_lag + int(np.argmax(ac[min_lag:max_lag]))
    period_s = peak * hop_ms / 1000.0
    bpm = 60.0 / period_s if period_s > 0 else 120.0

    beats = np.arange(0.0, len(f0_hz) * hop_ms / 1000.0, period_s, dtype=np.float32)
    return float(bpm), beats