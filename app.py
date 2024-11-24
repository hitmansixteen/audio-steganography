from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

from Algorithms.LSB import LSB  
from Algorithms.PhaseEncoding import PhaseCoding  
from Algorithms.DSSS.DSSS import DSSS
from Algorithms.EchoHiding import EchoHiding

root = Tk()

class Window(Frame):
    def __init__(self,master=None):

        Frame.__init__(self,master)
        self.master = master
        self.initWindow()

    def initWindow(self):
        
        self.master.title("Audio Steganography")
        self.pack(fill=BOTH, expand=1)
        self.drawEncoding()
        self.drawDecoding()

    def drawEncoding(self):
        
        self.encodeVar = StringVar()    
        self.encodeVar.set("Encoding ")
        self.encodeLabel = Label(root, textvariable=self.encodeVar)
        self.encodeLabel.place(x=10, y=10)

        self.optionsVar = StringVar()
        self.optionsVar.set("Least Significant Bit")

        self.encodingOptionsMenu = OptionMenu(root, self.optionsVar, "Least Significant Bit", "Phase Coding", "Spread Spectrum","Echo Hiding", "Parity Coding")
        self.encodingOptionsMenu.place(x=10, y=50)

        self.selectFileButton = Button(self, text="Select File to Encode", command=self.selectFile)
        self.selectFileButton.place(x=10, y=100)

        self.locationVar = StringVar()
        self.locationLabel = Label(root, textvariable=self.locationVar,relief=RAISED)
        self.locationLabel.place(x=10, y=130)

        self.entryText = Entry(root)
        self.entryText.place(x=10, y=180)
        self.entryText.insert(0, "Enter Message to Encode")

        self.encodeButton = Button(root, text="Encode", command=self.encode)
        self.encodeButton.place(x=10, y=220)

        self.encodedLocationVar = StringVar()
        self.encodedLocationLabel = Label(root, textvariable=self.encodedLocationVar)
        self.encodedLocationLabel.place(x=10, y=280)



    def drawDecoding(self):
        
        self.decodeVar = StringVar()
        self.decodeLabel = Label(root, textvariable=self.decodeVar)
        self.decodeLabel.place(x=500, y=10)
        self.decodeVar.set("Decoding")

        self.decodeOptionsVar = StringVar()
        self.decodeOptionsVar.set("Least Significant Bit")

        self.decodeOptionsMenu = OptionMenu(root, self.decodeOptionsVar, "Least Significant Bit", "Phase Coding", "Spread Spectrum","Echo Hiding", "Parity Coding")
        self.decodeOptionsMenu.place(x=500, y=50)

        self.selectFileDecodeButton = Button(root, text="Select File to Decode", command=self.selectFileDecode) 
        self.selectFileDecodeButton.place(x=500, y=100)

        self.decodeFileVar = StringVar()
        self.decodeFileLabel = Label(root, textvariable=self.decodeFileVar, relief=RAISED)
        self.decodeFileLabel.place(x=500, y=140)

        self.decodeButton = Button(root, text="Decode", command=self.decode)
        self.decodeButton.place(x=500, y=200)

        self.decodeStringVar = StringVar()
        self.decodeStringLabel = Label(root, textvariable=self.decodeStringVar, font=(None,30))
        self.decodeStringLabel.place(x=500, y=350) 

    def clientExit(self):
        exit()

    def selectFile(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select File to Encode", filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        self.fileSelected = root.filename
        self.locationVar.set("File Selected: " + self.fileSelected)

    def selectFileDecode(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select File to Decode", filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        self.fileSelectedDecode = root.filename
        self.decodeFileVar.set("File Selected: " + self.fileSelectedDecode)

    def encode(self):

        if self.optionsVar.get() == "Least Significant Bit":
            algo = LSB()
        elif self.optionsVar.get() == "Phase Coding":
            algo = PhaseCoding()
        elif self.optionsVar.get() == "Spread Spectrum":
            algo = DSSS()
        elif self.optionsVar.get() == "Echo Hiding":
            algo = EchoHiding()
        elif self.optionsVar.get() == "Parity Coding":
            pass

        result = algo.encode(self.fileSelected, self.entryText.get())

        self.encodedLocationVar.set("Encoded File Location: " + result)

    def decode(self):
        if self.decodeOptionsVar.get() == "Least Significant Bit":
            algo = LSB()
        elif self.decodeOptionsVar.get() == "Phase Coding":
            algo = PhaseCoding()
        elif self.decodeOptionsVar.get() == "Spread Spectrum":
            algo = DSSS()
        elif self.optionsVar.get() == "Echo Hiding":
            algo = EchoHiding()
            result = algo.decode(self.fileSelectedDecode, self.fileSelected, len(self.entryText.get().encode('utf-8'))*8)
            self.decodeStringVar.set(result)
            return
        elif self.optionsVar.get() == "Parity Coding":
            pass

        result = algo.decode(self.fileSelectedDecode)
        self.decodeStringVar.set(result)

        



root.geometry("1000x700")

app = Window(root)

root.mainloop()