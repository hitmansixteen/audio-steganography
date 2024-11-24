import warnings
import Algorithms.DSSS.utils as ut
from math import floor
import numpy as np
import Algorithms.DSSS.mixer as mixer

class DSSS:
    __num_reserved_bits = 40
    __key = '1234123412341234'
    __min_segment_len = 4*1024

    def encode(self,audioLocation,stringToEncode,alpha=0.002):

        bin_text = ut.text_to_bits(stringToEncode)

        original_signal, sample_rate = ut.read_audio(audioLocation)
        if len(original_signal.shape) == 2:
            return "Works only on mono audio files"

        signal_length = len(original_signal) - self.__num_reserved_bits
        msg_length = len(bin_text)

        segment_length = floor(signal_length/msg_length)
        segment_length = max(segment_length,self.__min_segment_len)

        num_segments = floor(signal_length/segment_length)
        num_segments = num_segments - (num_segments % 8)

        if msg_length > num_segments:
            warnings.warn("Message too long")
            return "Message too long"
        
        pn = self.__prng(segment_length)
        pn = np.reshape(pn,newshape=(segment_length,1))

        pn=np.reshape(pn*np.ones(shape=(1,num_segments),dtype='int'), newshape=(num_segments*segment_length),order='F')

        msg_sig_smooth,_ = mixer.mix(segment_length,bin_text,1,-1,256)

        pn_msg = msg_sig_smooth*pn

        steg_signal = original_signal[:num_segments*segment_length] + alpha * pn_msg

        signal_with_len = self.__embed_msg_len(original_signal,msg_length)
        steg_signal = np.append(steg_signal,signal_with_len[num_segments*segment_length:])

        steg_file_path = ut.write_audio_sf(steg_signal,sample_rate)

        return steg_file_path
    
    def decode(self,audioLocation):
        stego_signal, sample_rate = ut.read_audio(audioLocation)
        
        signal_length = len(stego_signal) - self.__num_reserved_bits

        msg_length = self.__extract_msg_len(stego_signal)   

        segment_length = floor(signal_length/msg_length)
        segment_length = max(segment_length,self.__min_segment_len)

        num_segments = floor(signal_length/segment_length)
        num_segments = num_segments - (num_segments % 8)

        signal_matrix = np.reshape(stego_signal[:num_segments*segment_length],(segment_length,num_segments),order='F')

        pn = self.__prng(segment_length)

        data = np.empty(shape = num_segments,dtype='str')

        for i in range(num_segments):
            corr = sum(signal_matrix[:,i]*pn)/segment_length

            if corr < 0:
                data[i] = '0'
            else:
                data[i] = '1'

        decoded_text = ut.bits_to_text(data)
        return decoded_text 
    
    def __embed_msg_len(self,original_signal,msg_length):
        signal_cpy = np.copy(original_signal)

        msg_length_bits = ut.bits_to_array('{0:040b}'.format(msg_length))

        max_s = max(signal_cpy[-self.__num_reserved_bits:])
        min_s = min(signal_cpy[-self.__num_reserved_bits:])

        for i in range(0,len(msg_length_bits)):
            if msg_length_bits[i] == 0:
                msg_length_bits[i] = min_s
            else:
                msg_length_bits[i] = max_s

        signal_cpy[-self.__num_reserved_bits:] = msg_length_bits

        return signal_cpy
    

    def __extract_msg_len(self,stego_signal):
        max_s = max(stego_signal[-self.__num_reserved_bits:])
        signal_slice = stego_signal[-self.__num_reserved_bits:]

        msg_length_bits = []

        for i in range(0,self.__num_reserved_bits):
            if signal_slice[i] == max_s:
                msg_length_bits.append(1)
            else:
                msg_length_bits.append(0)
        

        msg_length = ut.bits_to_integer(msg_length_bits)
        return msg_length
    

    def __prng(self,length):
        password = 0
        for i in range(len(self.__key)):
            password += ord(self.__key[i])*i
        
        np.random.seed(password)

        pn = 2* np.random.randint(2,size=length)-1

        return pn
    
