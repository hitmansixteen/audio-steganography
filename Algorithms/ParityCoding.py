import progressbar
import os
import wave

class ParityCoding:
        
    def _string_to_bin(self, message):
        binary_list = []
        for char in message:
            binary_char = bin(ord(char))[2:].zfill(8)
            binary_list.extend(map(int, binary_char))
        return binary_list
    
    def _bin_to_string(self, binary_list):
        characters = [
            chr(int("".join(map(str, binary_list[i:i + 8])), 2))
            for i in range(0, len(binary_list), 8)
        ]
        return ''.join(characters)

    def _len_mess_to_bytes(self, length):
        return length.to_bytes(4, 'big')

    def _check_parity_encode(self, a, b, bit):
        combined = f'{bin(a)[2:].zfill(8)}{bin(b)[2:].zfill(8)}'
        parity_bit = int(combined[-1])
        count = combined[:-1].count('1')
        if (count % 2 == 0 and bit == 1) or (count % 2 == 1 and bit == 0):
            parity_bit = 1
        else:
            parity_bit = 0
        new_combined = combined[:-1] + str(parity_bit)
        return int(new_combined[:8], 2), int(new_combined[8:], 2)
    
    def _check_parity_decode(self, a, b):
        combined = f'{bin(a)[2:].zfill(8)}{bin(b)[2:].zfill(8)}'
        return combined.count('1') % 2

    def encode(self, fileLocation, message):
        self.audio = wave.open(fileLocation, "rb")
        audio_data = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        
        if len(audio_data) < len(message) * 16 + 7:
            raise ValueError("Message is too large to embed in this audio file.")
        
        message_bin = self._string_to_bin(message)
        message_len_bytes = self._len_mess_to_bytes(len(message))
        
        bar = progressbar.ProgressBar()
        
        # Add message length 
        audio_data[:4] = bytes(message_len_bytes)
        
        # Encode the message
        index = 4  # Start encoding after the message length
        for bit in bar(message_bin):
            a, b = audio_data[index], audio_data[index + 1]
            audio_data[index], audio_data[index + 1] = self._check_parity_encode(a, b, bit)
            index += 2

        return self.saveFile(audio_data, fileLocation)


    
    def decode(self, fileLocation):
        self.audio = wave.open(fileLocation, "rb")
        audio_data = bytearray(list(self.audio.readframes(self.audio.getnframes())))
            
        # Extract the message length from the first 4 bytes
        message_length = int.from_bytes(audio_data[:4], 'big')
        total_bits = message_length * 8  # Total number of bits in the message
        
        decoded_bits = []
        index = 4  # Start after the length header

        for _ in range(total_bits):
            a, b = audio_data[index], audio_data[index + 1]
            bit = self._check_parity_decode(a, b)  # Get the embedded bit
            decoded_bits.append(bit)
            index += 2

        # Convert binary list to string
        decoded_message = self._bin_to_string(decoded_bits)
        
        return decoded_message





    def saveFile(self, audioArr, location):
            
        dir = os.path.dirname(location)
        self.newAudio = wave.open(dir + "/parity-coding.wav", "wb")
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audioArr)
        self.newAudio.close()
        self.audio.close()
        return dir + "/parity-coding.wav"