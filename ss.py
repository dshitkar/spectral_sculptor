import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import stft, istft

def spectral_morph(audio1, audio2, morph_ratios, grain_size):
    # **1. STFT Analysis**
    _, _, Zxx1 = stft(audio1, window='hann', nperseg=grain_size * 2, noverlap=grain_size)
    _, _, Zxx2 = stft(audio2, window='hann', nperseg=grain_size * 2, noverlap=grain_size)

    # **2. Spectral Morphing**
    Zxx_morphed = (1 - morph_ratios) * Zxx1 + morph_ratios * Zxx2  # Linear blending

    # **3. IFFT Synthesis**
    _, audio_morphed = istft(Zxx_morphed)
    return audio_morphed
