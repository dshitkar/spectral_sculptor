'''Copyright (c) 2024 - Dhananjay Shitkar for Portland State University 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Welcome to Spectral Sculptor

# Import the important stuff

import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import stft, istft
import soundfile as sf
import librosa

# Loading our audio files

def load_audio(filename):
    audio_data, samplerate = sf.read(filename) 

    if samplerate != 48000:  # Resample if not already at 48000 Hz
         audio_data = librosa.resample(audio_data, orig_sr=samplerate, target_sr=48000)
         samplerate = 48000 

    return audio_data, samplerate 

# Saving our audio file

def save_audio(audio_data, filename, samplerate):
    sf.write(filename, audio_data, samplerate)

# This is where the magic happens (STFT)
    
def spectral_morph(audio1, audio2, morph_ratios, grain_size):
    nperseg = 512  # Adjust if needed
    noverlap = nperseg // 2 

    _, _, Zxx1 = stft(audio1, window='hann', nperseg=nperseg, noverlap=noverlap)
    _, _, Zxx2 = stft(audio2, window='hann', nperseg=nperseg, noverlap=noverlap)

    # We need to ensure STFT outputs have compatible shapes for interpolation

    if Zxx1.shape != Zxx2.shape:
        raise ValueError("STFT outputs have incompatible shapes for morphing.")

    # Spectral Interpolation
    Zxx_morphed = (1 - morph_ratios) * Zxx1 + morph_ratios * Zxx2

    # Inverse Short-Time Fourier Transform (ISTFT)
    _, audio_morphed = istft(Zxx_morphed, window='hann', nperseg=nperseg, noverlap=noverlap)

    return audio_morphed

# This is for our UI

def load_file1():
    filename = filedialog.askopenfilename(title="Select Audio File 1")
    global audio_data1, samplerate1 
    audio_data1, samplerate1 = load_audio(filename)
    file1_label.config(text=f"Loaded: {filename}")

def load_file2():
    filename = filedialog.askopenfilename(title="Select Audio File 2")
    global audio_data2, samplerate2 
    audio_data2, samplerate2 = load_audio(filename)
    file2_label.config(text=f"Loaded: {filename}")

def create_frequency_controls():
    global band1_slider
    band1_slider = tk.Scale(window, label="Band 1", from_=0, to=24000, resolution=100, orient=tk.HORIZONTAL)  
    band1_slider.pack()


def create_grain_size_control():
    global grain_size_slider
    grain_size_slider = tk.Scale(window, label="Grain Size", from_=128, to_=4096, orient=tk.HORIZONTAL)
    grain_size_slider.pack()

def process_and_save():
    global audio_data1, audio_data2

    if audio_data1 is not None and audio_data2 is not None:

        # Ensure same length before morphing
        audio_data1, audio_data2 = ensure_same_length(audio_data1, audio_data2) 

        band1_value = band1_slider.get()

        grain_size = grain_size_slider.get()

        morph_ratios = 0.5 
        _, _, Zxx1 = stft(audio_data1, window='hann')
        _, _, Zxx2 = stft(audio_data2, window='hann')

        Zxx1[50:100, :] *= band1_value / 100  # Adjust indices as needed based on your bands

        Zxx_morphed = (1 - morph_ratios) * Zxx1 + morph_ratios * Zxx2
        _, audio_morphed = istft(Zxx_morphed)

        filename = filedialog.asksaveasfilename(title="Save Morphed Audio") # Preferably save as .wav
        save_audio(morphed_audio, filename, samplerate1)  
    else:
        print("Please load both audio files first.")

def ensure_same_length(audio_data1, audio_data2):
    min_length = min(len(audio_data1), len(audio_data2))
    return audio_data1[:min_length], audio_data2[:min_length] 

audio_data1, audio_data2 = None, None
samplerate1, samplerate2 = None, None

# Tkinter UI Setup
window = tk.Tk()
window.title("Spectral Sculptor")

load_button1 = tk.Button(text="Load Audio 1", command=load_file1)
load_button1.pack()
file1_label = tk.Label(text="")
file1_label.pack()

load_button2 = tk.Button(text="Load Audio 2", command=load_file2)
load_button2.pack()
file2_label = tk.Label(text="")
file2_label.pack()

create_frequency_controls()
create_grain_size_control()

process_button = tk.Button(text="Morph & Save", command=process_and_save)
process_button.pack()

window.mainloop()