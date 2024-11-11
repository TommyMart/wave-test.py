import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from distortion import apply_distortion

# Load audio file
audio_data, sample_rate = librosa.load("test_audio.wav", sr=None, mono=False)

# Check if audio is mono or stereo
if audio_data.ndim == 1:
    # Mono
    print("Audio is mono.")
    distorted_audio = apply_distortion(audio_data, sample_rate)
else:
    # Stereo
    print("Audio is stereo.")
    left_channel = apply_distortion(
        audio_data[0, :], sample_rate).astype(np.float32)
    right_channel = apply_distortion(
        audio_data[1, :], sample_rate).astype(np.float32)

    # Ensure both channels have the same shape and stack them
    min_length = min(len(left_channel), len(right_channel))
    left_channel = left_channel[:min_length]
    right_channel = right_channel[:min_length]
    distorted_audio = np.vstack(
        (left_channel, right_channel)).astype(np.float32)

# Transpose if necessary to shape (num_samples, num_channels)
if distorted_audio.ndim == 2 and distorted_audio.shape[0] == 2:
    distorted_audio = distorted_audio.T

# Define target sample rate used in apply_downsampling
target_rate = 8000

# Save distorted audio
sf.write("distorted_audio.wav", distorted_audio, target_rate)

# Plot the original and distorted waveforms for comparison
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(audio_data[0] if audio_data.ndim > 1 else audio_data)
plt.title("Original Audio (Left Channel Only)")

plt.subplot(2, 1, 2)
plt.plot(distorted_audio[:, 0]
         if distorted_audio.ndim > 1 else distorted_audio)
plt.title("Distorted Audio (Left Channel Only)")

plt.show()
