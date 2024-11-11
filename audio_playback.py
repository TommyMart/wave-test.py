import librosa
import soundfile as sf
import apply_distortion from './distortion'
import matplotlib.pyplot as plt

# Load audio file
audio_data, sample_rate = librosa.load("test_audio.wav", sr=None)

# Apply distortion effect
distorted_audio = apply_distortion(audio_data, sample_rate)

# Save distorted audio
sf.write("distorted_audio.wav", distorted_audio, sample_rate)

# Plot the original and distorted waveforms for comparison
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(audio_data)
plt.title("Original Audio")

plt.subplot(2, 1, 2)
plt.plot(distorted_audio)
plt.title("Distorted Audio")

plt.show()
