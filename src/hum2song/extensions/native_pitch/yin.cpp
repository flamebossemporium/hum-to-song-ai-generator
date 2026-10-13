// YIN pitch extractor. C++20. Compiled into yinyin.dll / libyinyin.so.
// Exposed via ctypes from hum2song/extensions/native_pitch/binding.py.
#include <cmath>
#include <cstddef>
#include <vector>

extern "C" int yin_extract(
    const float* audio,
    int n_samples,
    int sample_rate,
    int frame,
    float* f0_out,
    float* conf_out)
{
    if (n_samples < frame || frame <= 0) return -1;
    const int hop = frame / 2;
    const int n_frames = (n_samples - frame) / hop + 1;
    const int tau_min = sample_rate / 1000;   // 1000 Hz ceiling
    const int tau_max = sample_rate / 60;     // 60 Hz floor

    std::vector<float> diff(tau_max, 0.0f);
    std::vector<float> cmnd(tau_max, 0.0f);

    for (int i = 0; i < n_frames; ++i) {
        const float* win = audio + i * hop;
        float running = 0.0f;
        cmnd[0] = 1.0f;
        for (int tau = tau_min; tau < tau_max; ++tau) {
            float d = 0.0f;
            for (int j = 0; j < frame - tau; ++j) {
                const float delta = win[j] - win[j + tau];
                d += delta * delta;
            }
            diff[tau] = d;
            running += d;
            cmnd[tau] = (running > 0.0f) ? d * tau / running : 0.0f;
        }

        int best_tau = -1;
        for (int tau = tau_min + 1; tau < tau_max - 1; ++tau) {
            if (cmnd[tau] < 0.15f &&
                cmnd[tau] < cmnd[tau - 1] &&
                cmnd[tau] < cmnd[tau + 1]) {
                best_tau = tau;
                break;
            }
        }
        if (best_tau > 0) {
            f0_out[i] = static_cast<float>(sample_rate) / best_tau;
            conf_out[i] = 1.0f - cmnd[best_tau];
        } else {
            f0_out[i] = 0.0f;
            conf_out[i] = 0.0f;
        }
    }
    return 0;
}