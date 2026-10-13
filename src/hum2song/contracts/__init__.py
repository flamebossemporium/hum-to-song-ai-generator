"""Shared contracts every extension implements."""
from hum2song.contracts.pitch import PitchExtension, PitchResult
from hum2song.contracts.vocode import VocodeExtension
from hum2song.contracts.formant import FormantExtension

__all__ = ["PitchExtension", "PitchResult", "VocodeExtension", "FormantExtension"]