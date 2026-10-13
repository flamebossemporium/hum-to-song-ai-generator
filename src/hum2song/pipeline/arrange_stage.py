"""Arrange stage: quantize pitch to a scale and lay out bars."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

MAJOR = np.array([0, 2, 4, 5, 7, 9, 11], dtype=np.float32)


@dataclass(frozen=True)
class Arrangement:
    notes_midi: np.ndarray
    note_starts_s: np.ndarray
    note_durations_s: np.ndarray
    bpm: float


def _hz_to_midi(f0_hz: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return 69.0 + 12.0 * np.log2(f0_hz / 440.0)


def _snap_to_scale(midi: np.ndarray, root: int = 60) -> np.ndarray:
    snapped = np.empty_like(midi)
    for i, m in enumerate(midi):
        if np.isnan(m):
            snapped[i] = np.nan
            continue
        pc = (int(round(m)) - root) % 12
        nearest = MAJOR[np.argmin(np.abs(MAJOR - pc))]
        snapped[i] = round(m) - pc + nearest
    return snapped


def run_arrange_stage(
    f0_hz: np.ndarray,
    hop_ms: float,
    bpm: float,
    beats: np.ndarray,
) -> Arrangement:
    midi = _snap_to_scale(_hz_to_midi(f0_hz))
    voiced = ~np.isnan(midi)
    starts, durations, notes = [], [], []
    i = 0
    while i < len(midi):
        if not voiced[i]:
            i += 1
            continue
        j = i
        while j < len(midi) and voiced[j] and abs(midi[j] - midi[i]) < 0.6:
            j += 1
        starts.append(i * hop_ms / 1000.0)
        durations.append((j - i) * hop_ms / 1000.0)
        notes.append(float(midi[i]))
        i = j
    return Arrangement(
        notes_midi=np.array(notes, dtype=np.float32),
        note_starts_s=np.array(starts, dtype=np.float32),
        note_durations_s=np.array(durations, dtype=np.float32),
        bpm=bpm,
    )