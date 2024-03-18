# Spectral Sculptor

**By Dan Shitkar (PSU/Odin ID: [930527770/dshitkar])**

## Project Overview

The Spectral Sculptor lets you seamlessly morph between two different audio sources.  Dive into the frequency domain and reshape sounds like never before, blending elements of your favorite recordings to create entirely new sonic textures. Whether you're a musician seeking unique soundscapes, a sound designer crafting otherworldly effects, or simply an audio enthusiast, Spectral Sculptor puts a world of sonic transformation at your fingertips.

## Status

- **Completed:**
  - Loading Audio Files: My code fully handles loading audio files of various formats, resampling them if necessary for consistency.
  - Core STFT Functionality: The code has the basic structure for calculating the STFT and the ISTFT for reconstructing the morphed audio signal.
  - UI Foundation: I've set up the UI with sliders for frequency band control, ready to be integrated with spectral manipulation logic along with a grain size control slider.
 
- **Remainging:**
  - Real-Time STFT
 
- **Satisfaction:**
  - Listening to the end-product, I am very happy with my result (because it sounds really cool). If I had the time and energy, being able to implement the real-time STFT would've been great. Additionally, I would've loved to add a real-time spectrogram.
 
## Example

```
# Load audio files
audio1 = load_audio("sound1.wav")
audio2 = load_audio("sound2.wav")

# Set morph ratios and frequency band manipulations
morph_ratios = 0.75  # More emphasis on audio2
band1_value = 0.3  # Reduce low frequencies from audio1

# Adjust grain size for a slightly granular effect
grain_size = 1024 

# Perform the morphing magic!
morphed_audio = spectral_morph(audio1, audio2, morph_ratios, grain_size)

# Save the result
save_audio(morphed_audio, "sound3.wav")
```

## Build Instructions

### Prerequisites

- Python 3.x
- Required libraries: `numpy`, `scipy`, 'tkinter', 'soundfile', 'librosa'

**Installation:**

1. Clone the Repository:  Obtain a copy of the Spectral Sculptor project repository using Git:
```
git clone https://github.com/dshitkar/spectral_sculptor
```
2. Install the necessary libraries:

   ```bash
   pip install numpy scipy  tkinter soundfile librosa
   ```

**Running the Code:**

2. Navigate to the project directory in your terminal.

3. Execute the Python script:

   ```bash
   python ss.py
   ```
**License**

This project is licensed under the [MIT License](spectral_sculptor/LICENSE.txt).
