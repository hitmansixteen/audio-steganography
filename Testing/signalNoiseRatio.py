import wave
import numpy as np

def calculate_snr(original_audioLocation, stego_audioLocation):
    original_audio = wave.open(original_audioLocation, "rb")
    stego_audio = wave.open(stego_audioLocation, "rb")

    original_data = np.frombuffer(original_audio.readframes(original_audio.getnframes()), dtype=np.int16)
    stego_data = np.frombuffer(stego_audio.readframes(stego_audio.getnframes()), dtype=np.int16)

    min_length = min(len(original_data), len(stego_data))
    original_data = original_data[:min_length]
    stego_data = stego_data[:min_length]


    noise = original_data - stego_data
    signal_power = np.sum(original_data ** 2)
    noise_power = np.sum(noise ** 2)

    if noise_power == 0:
        return "SNR is infinite: Perfect Signal!!!"

    snr = 10 * np.log10(signal_power / noise_power)
    return snr
