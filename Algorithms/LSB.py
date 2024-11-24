import os.path
import wave

class LSB():

    def encode(self, audioLocation, stringToEncode):
        audioArray = self.convertToByteArray(audioLocation)

        stringToEncode = stringToEncode + int((len(audioArray) - (len(stringToEncode)*8*8))/8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in stringToEncode])))

        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit
        encodedAudio = bytes(audioArray)

        return self.saveFile(encodedAudio, audioLocation)


    def decode(self, audioLocation):
        
        audioArray = self.convertToByteArray(audioLocation)
        decodeArray = [audioArray[i] & 1 for i in range(len(audioArray))]
        self.audio.close()

        return ''.join(chr(int(''.join(map(str, decodeArray[i:i+8])), 2)) for i in range(0, len(decodeArray), 8)).split('###')[0]

    def convertToByteArray(self, audioLocation):
        self.audio = wave.open(audioLocation, "rb")
        audioArr = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        return audioArr

    def saveFile(self, audioArr, location):
        
        dir = os.path.dirname(location)
        self.newAudio = wave.open(dir + "/output-lsb.wav", "wb")
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audioArr)
        self.newAudio.close()
        self.audio.close()
        return dir + "/output-lsb.wav"
