// Hum2Song.Vocodec — WORLD-style vocoder core. .NET 8, nullable enabled.
// Called from Python via pythonnet; see binding.py.
using System;

namespace Hum2Song.Vocodec
{
    public sealed class Renderer
    {
        private readonly float _breathiness;
        private readonly float _vibratoHz;

        public Renderer(float breathiness, float vibratoHz)
        {
            _breathiness = breathiness;
            _vibratoHz = vibratoHz;
        }

        public float[] Render(float[] f0Hz, float[] envelope, int sampleRate)
        {
            if (f0Hz.Length != envelope.Length)
                throw new ArgumentException("f0 and envelope length mismatch");

            var output = new float[f0Hz.Length];
            var rng = new Random(0);
            double phase = 0.0;
            double vibPhase = 0.0;

            for (int i = 0; i < f0Hz.Length; i++)
            {
                float f0 = f0Hz[i];
                if (f0 <= 0f)
                {
                    output[i] = 0f;
                    continue;
                }
                double vib = 1.0 + 0.008 * Math.Sin(vibPhase);
                vibPhase += 2.0 * Math.PI * _vibratoHz / sampleRate;
                phase += 2.0 * Math.PI * f0 * vib / sampleRate;

                double tone = Math.Sin(phase);
                double breath = (rng.NextDouble() * 2.0 - 1.0) * _breathiness;
                output[i] = (float)((tone + breath) * envelope[i]);
            }
            return output;
        }
    }
}