import wave


# - number of channels
# - sample width
# - framerate / sample rate: 44,100 Hz (sample values each second)
# - number of frames
# - values of a frame

# Open the wave file
obj = wave.open("test_audio.wav", "rb")

# Print audio file metadata
print("Number of channels:", obj.getnchannels())
print("Sample width:", obj.getsampwidth())
print("Frame rate:", obj.getframerate())
print("Number of frames:", obj.getnframes())
print("Params:", obj.getparams())

# Calculate the total audio duration
time_audio = obj.getnframes() / obj.getframerate()
print("Audio duration (seconds):", time_audio)

# Read all frames in the file
frames = obj.readframes(-1)

# Calculate the number of frames based on sample width and channels
num_channels = obj.getnchannels()
sample_width = obj.getsampwidth()  # 3 bytes per sample
total_samples = len(frames) / (sample_width * num_channels)

print("Total number of samples:", total_samples)

# Close the wave file
obj.close()

# Create new audio files based on obj params
obj_new = wave.open("test_audio_new.wav", "wb")

obj_new.setnchannels(2)
obj_new.setsampwidth(3)
obj_new.setframerate(48000)

obj_new.writeframes(frames)

obj_new.close
