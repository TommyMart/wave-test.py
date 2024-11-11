import numpy as np
import wave
import matplotlib as plt
from scipy.signal import resample

# Main distortion function applying a chain of all unique distortion sounds to audio_data


def apply_distortion(audio_data, sample_rate):
    # 1. Apply clipping (0 - 1)
    # A higher threshold will allow more of the original signal’s peaks to pass through, reducing the harshness of the distortion.
    audio_data = apply_clipping_dist(audio_data, threshold=.8)

    # 2. Apply bit depth reduction (1 - 16)
    # Increasing the bit depth will preserve more detail in the audio, making it sound less “crunchy” and more natural.
    audio_data = apply_bit_depth_reduction(audio_data, bit_depth=10)

    # 3. Apply overdrive (1.0 - 10.0<)
    # Reducing the gain will make the overdrive effect less intense, producing softer clipping.
    audio_data = apply_overdrive(audio_data, gain=1)

    # 4. Apply down sampling
    # A higher target sample rate will reduce the “crunchiness” introduced by downsampling while still affecting the sound quality subtly.
    audio_data = apply_downsampling(
        audio_data, original_rate=sample_rate, target_rate=8000)

    return audio_data


# Clipping Distortion
# Clipping cuts off the amplitude peaks of the waveform, creating a harsher, more distorted sound.


def apply_clipping_dist(audio_data, threshold=0.3):
    # Apply clipping by limiting the max amplitude
    clipped_audio = np.clip(audio_data, -threshold, threshold)
    return clipped_audio

# Bit Depth Reduction
# Reducing the bit depth of the audio signal introduces quantization error, resulting in a gritty, "lo-fi" sound.


def apply_bit_depth_reduction(audio_data, bit_depth=4):
    # Scale audio from -1 to 1
    audio_min = np.min(audio_data)
    audio_max = np.max(audio_data)
    audio_data = 2 * (audio_data - audio_min) / (audio_max - audio_min) - 1

    # Quantize to the reduced bit depth
    max_val = 2 ** (bit_depth - 1) - 1
    audio_quantized = np.round(audio_data * max_val) / max_val

    # Scale back to original amplitude range
    audio_data = (audio_quantized + 1) * \
        (audio_max - audio_min) / 2 + audio_min
    return audio_data

# Overdrive (Non-linear distortion)
# Overdrive introduces a kind of soft clipping, producing a distortion effect without the harsh clipping of hard clipping. This is common in analog and tube amplifiers.


def apply_overdrive(audio_data, gain=2.0):
    # Apply gain to increase amplitude
    audio_ampliphied = gain * audio_data

    # Apply a non-linear transformation for softer clipping
    # tanh = tanh ( x ) = sinh ( x ) cosh ( x ) = e 2 x − 1 e 2 x + 1
    overdrive_audio = np.tanh(audio_ampliphied)
    return overdrive_audio

# Downsampling (Reduxing Sample Size)
# Lowering the sample rate reduces the quality and introduces a distorted, "crunchy" sound. This can be combined with bit depth reduction for a more dramatic effect.


def apply_downsampling(audio_data, original_rate, target_rate):
    # Calc the new length for downsampling
    num_samples = int(len(audio_data) * target_rate / original_rate)
    downsampled_audio = resample(audio_data, num_samples)

    return downsampled_audio
