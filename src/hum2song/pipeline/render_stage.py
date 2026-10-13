"""Render stage: vocode notes with the loaded vocode extension."""
from __future__ import annotations

import numpy as np

from hum2song.host.loader import ExtensionLoader
from hum2song.pipeline.arrange_stage import Arrangement


def _midi_to_hz(midi: np.ndarray) -> np.ndarray:
    return 440.0 * np.power(2.0, (midi - 69.0) / 12.0)


def run_render_stage(
    arrangement: Arrangement,
    loader: ExtensionLoader,
    sample_rate: int = 44100,
    preferred: str = "dotnet_vocodec",
) -> np.ndarray:
    """Build an f0 track + envelope, hand to the vocode extension."""
    total_s = float(
        (arrangement.note_starts_s + arrangement.note_durations_s).max()
        if len(arrangement.notes_midi)
        else 0.0
    )
    n = int(total_s * sample_rate)
    f0 = np.zeros(n, dtype=np.float32)
    env = np.zeros(n, dtype=np.float32)

    for midi, start, dur in zip(
        arrangement.notes_midi,
        arrangement.note_starts_s,
        arrangement.note_durations_s,
    ):
        a = int(start * sample_rate)
        b = min(n, a + int(dur * sample_rate))
        if b <= a:
            continue
        f0[a:b] = _midi_to_hz(np.array([midi], dtype=np.float32))[0]
        env[a:b] = np.hanning(b - a).astype(np.float32)

    try:
        ext = loader.get(preferred)
    except KeyError:
        if not loader.loaded:
            raise RuntimeError("no vocode extension loaded") from None
        ext = next(iter(loader.loaded.values()))
    return ext.render(f0, env, sample_rate)