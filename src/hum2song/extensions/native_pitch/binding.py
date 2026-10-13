"""ctypes binding to the C++ YIN pitch extractor."""
from __future__ import annotations

import ctypes
from pathlib import Path

import numpy as np

from hum2song.contracts.pitch import PitchResult

_LIB = Path(__file__).parent / "build" / "libyinyin.so"
if not _LIB.is_file():
    _LIB = Path(__file__).parent / "build" / "yinyin.dll"

_lib = ctypes.CDLL(str(_LIB)) if _LIB.is_file() else None
if _lib is not None:
    _lib.yin_extract.argtypes = [
        ctypes.POINTER(ctypes.c_float),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float),
    ]
    _lib.yin_extract.restype = ctypes.c_int


class NativePitch:
    name = "native_pitch"

    def __init__(self, options: dict) -> None:
        self.frame_ms = int(options.get("frame_ms", 32))
        self.threshold = float(options.get("threshold", 0.15))

    def extract(self, audio: np.ndarray, sample_rate: int) -> PitchResult:
        if _lib is None:
            raise RuntimeError("native_pitch shared library not built")
        frame = int(sample_rate * self.frame_ms / 1000)
        hop = frame // 2
        n_frames = max(0, (len(audio) - frame) // hop + 1)
        f0 = np.zeros(n_frames, dtype=np.float32)
        conf = np.zeros(n_frames, dtype=np.float32)
        audio_f32 = np.ascontiguousarray(audio, dtype=np.float32)
        rc = _lib.yin_extract(
            audio_f32.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            len(audio_f32),
            sample_rate,
            frame,
            f0.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            conf.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        )
        if rc != 0:
            raise RuntimeError(f"yin_extract failed rc={rc}")
        f0[f0 <= 0] = np.nan
        return PitchResult(f0_hz=f0, hop_ms=hop * 1000.0 / sample_rate, confidence=conf)


def build(options: dict) -> NativePitch:
    return NativePitch(options)