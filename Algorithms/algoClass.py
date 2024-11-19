from abc import ABC, abstractmethod

class AlgoClass(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def encode(self, audioLocation, stringToEncode) ->str:
        pass

    @abstractmethod
    def decode(self, audioLocation) -> str:
        pass

    @abstractmethod
    def convertToByteArray(self,audio):
        pass

    @abstractmethod
    def saveFile(self, audioArr, location)->str:
        pass

