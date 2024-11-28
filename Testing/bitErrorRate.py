import numpy as np
import wave

def calculate_ber(original_audioLocation, stego_audioLocation):

    original_audio = wave.open(original_audioLocation, "rb")
    stego_audio = wave.open(stego_audioLocation, "rb")

    original_data = bytearray(list(original_audio.readframes(original_audio.getnframes())))
    extracted_data = bytearray(list(stego_audio.readframes(stego_audio.getnframes())))

    errors = sum(o != e for o, e in zip(original_data, extracted_data))
    total_bits = len(original_data)
    
    ber = errors / total_bits
    return ber