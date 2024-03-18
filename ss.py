import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import stft, istft
import soundfile as sf

def load_audio(filename):
    audio_data, samplerate = sf.read(filename)
    return audio_data, samplerate

def save_audio(audio_data, filename, samplerate):
    sf.write(filename, audio_data, samplerate)

def spectral_morph(audio1, audio2, morph_ratios, grain_size):
    _, _, Zxx1 = stft(audio1, window='hann', nperseg=grain_size * 2, noverlap=grain_size)
    _, _, Zxx2 = stft(audio2, window='hann', nperseg=grain_size * 2, noverlap=grain_size)

    Zxx_morphed = (1 - morph_ratios) * Zxx1 + morph_ratios * Zxx2
    _, audio_morphed = istft(Zxx_morphed)
    return audio_morphed

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

def process_and_save():
    if audio_data1 is not None and audio_data2 is not None:
        # Placeholder - You'll need UI controls for morph_ratios and grain_size
        morph_ratios = 0.5  # Example: Morph halfway between sounds
        grain_size = 1024

        morphed_audio = spectral_morph(audio_data1, audio_data2, morph_ratios, grain_size)

        filename = filedialog.asksaveasfilename(title="Save Morphed Audio")
        save_audio(morphed_audio, filename, samplerate1)  # Assuming same sample rate
    else:
        #  Handle the case when one or both files are missing (error message, etc.)
        print("Please load both audio files first.")

# Global variables (ideally, find a better way to manage state)
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

process_button = tk.Button(text="Morph & Save", command=process_and_save)
process_button.pack()

window.mainloop()
