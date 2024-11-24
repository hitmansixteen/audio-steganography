import soundfile as sf
import numpy as np

def text_to_bits(text):
    b_arr = bytearray(text, 'utf-8')
    res = ''.join(format(i, '08b') for i in b_arr)
    return res

def read_audio(audioLocation): 
    data, sample_rate = sf.read(audioLocation)
    return data, sample_rate

def write_audio_sf(data, sample_rate):
    sf.write('output-dsss.wav', data, sample_rate)
    return 'output-dsss.wav'

def bits_to_integer(bits):
    res = 0
    for bit in bits:
        res = (res << 1) | int(bit)
    return res

def bits_to_text(bits):
    text = ""
    bytes_arr = np.split(bits,int(len(bits)/8))
    for c_arr in bytes_arr:
        c = ''.join(c_arr)
        text += chr(int(c,base=2))
    return text

def bits_to_array(bits):    
    return list(int(i) for i in list(bits))