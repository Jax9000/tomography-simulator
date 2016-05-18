import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkFileDialog import askopenfilename
from matplotlib.figure import Figure
from skimage.io import imread
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class View:
    plotNames = ['', 'Original picture', 'Sinogram', 'Reconstruction', 'Difference']

    def __init__(self):
        self.root = Tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.wm_title("Embedding in TK")

        menubar = Tk.Menu(self.root)
        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load", command=self.__loadFile)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        self.f = Figure(figsize=(10, 5), dpi=100)
        for i in range(1, 5):
            self.subPlot = self.f.add_subplot(220 + i)
            self.subPlot.set_title(self.plotNames[i])
            self.subPlot.axis('off')
            print self.plotNames[i]

        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(columnspan=3)

        # canvas.mpl_connect('key_press_event', _on_key_event)

        self.detectors = Tk.Scale(self.root, from_=1, to=100, label='Detectors', orient=Tk.HORIZONTAL, command=self.__detectorEvent)
        self.detectors.grid(row=1, column=0)

        self.angle = Tk.Scale(self.root, from_=1, to=180, label='Angle', orient=Tk.HORIZONTAL, command=self.__angleEvent)
        self.angle.grid(row=1, column=1)

        self.scans = Tk.Scale(self.root, from_=1, to=1000, label='Scans', orient=Tk.HORIZONTAL, command=self.__scansEvent)
        self.scans.grid(row=1, column=2)

        b = Tk.Button(self.root, text="Start", command=self.__startEvent)
        b.grid(column=1)

    def start(self):
        Tk.mainloop()

    def setSubPlot(self, array, number):
        if(number < 1 or number > 5):
            raise ValueError('Plot number must be between 1 and 5')
            return
        number += 220 # requried for add_subplot function which has 2x2 subplots
        self.subPlot = self.f.add_subplot(number)
        self.subPlot.imshow(array)
        self.canvas.draw()

    def getDetectors(self):
        return self.detectors.get()

    def getAngle(self):
        return self.angle.get()

    def getScans(self):
        return self.scans.get()

    def __detectorEvent(self, value):
        return

    def __angleEvent(self, value):
        return

    def __scansEvent(self, value):
        return

    def __startEvent(self):
        print 'button pushed!'

    def __loadFile(self):
        Tk.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        return filename