import tkinter as tk
from tkinter import *

import cv2

import _thread
import serial

class interface:
    def __init__(self):
        self.window = tk.Tk()
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.w, self.h))

        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        self.window.title("IHM par ADTP")

        self.sachet_ok = tk.StringVar()
        self.manquant = tk.StringVar()
        self.trop = tk.StringVar()
        self.fiche = tk.StringVar()

        # frame 1
        self.frame1 = Frame(self.window, borderwidth=2)
        self.frame1.pack(padx=20, pady=20)


        # frame 2
        self.frame2 = Frame(self.window, borderwidth=2)
        self.frame2.pack(padx=20, pady=20)

        # frame 3
        self.frame3 = Frame(self.window, borderwidth=2)
        self.frame3.pack(padx=20, pady=20)

        # frame 4
        self.frame4 = Frame(self.window, borderwidth=2)
        self.frame4.pack(padx=20, pady=20)


        self.label1 = Label(self.frame1, text="Conformité du sachet ", width="300", height="2", font=("Calibri", 13))
        self.label_ok = Label(self.frame1,textvariable=self.sachet_ok,width="300", height="2", font=("Calibri", 13))
        self.label2 = Label(self.frame2, text="Pièces manquantes: ", width="300", height="2", font=("Calibri", 13))
        self.label_manquant = Label(self.frame2, textvariable=self.manquant, width="300", height="2", font=("Calibri", 13))
        self.label3 = Label(self.frame3, text="Pièces en trop: ", width="300", height="2", font=("Calibri", 13))
        self.label_trop = Label(self.frame3, textvariable=self.trop, width="300", height="1",font=("Calibri", 13))
        self.label4 = Label(self.frame4, text="Fiche de pièces sélectionnée: ", width="300", height="2", font=("Calibri", 13))
        self.label_fiche = Label(self.frame4, textvariable=self.fiche, width="300", height="2",font=("Calibri", 13))

        self.label1.pack(padx=10, pady=10)
        self.label_ok.pack(padx=10, pady=10)
        self.label2.pack(padx=10, pady=10)
        self.label_manquant.pack(padx=10, pady=10)
        self.label3.pack(padx=10, pady=10)
        self.label_trop.pack(padx=10, pady=10)
        self.label4.pack(padx=10, pady=10)
        self.label_fiche.pack(padx=10, pady=10)

        self.window.after(2000, _thread.start_new_thread, self.ChangeLabels, ())
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def ChangeLabels(self):

        while(1):
            serialString = serialPort.readline()
            serialString = serialString.decode('Ascii')
            serialString = serialString[0:len(serialString) - 1]
            self.sachet_ok.set(str("okokoko"))
            self.manquant.set(str("mmmm"))
            self.trop.set(str("tttt"))
            self.fiche.set(str("fff"))

if __name__ == '__main__':
    serialPort = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1.0)
    app = interface()
    serialPort.close()