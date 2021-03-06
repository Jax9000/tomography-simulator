import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkFileDialog import askopenfilename
from matplotlib.figure import Figure
from skimage.io import imread
import matplotlib.pyplot as plt
import sys
import tkMessageBox
from skimage.measure import compare_ssim as ssim
from skimage.transform import rescale

from tomograph import ParallelComputedTomography

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class View:
    plotNames = ['', 'Original picture', 'Sinogram', 'Reconstruction', 'Difference']

    def __init__(self):
        self.ct = ParallelComputedTomography(200, 180, 300)
        self.image = None

        self.root = Tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.wm_title("Computed Tomography Simulator")
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit())

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

        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(columnspan=4)

        self.detectors = Tk.Scale(self.root, from_=1, to=300, label='Detectors', orient=Tk.HORIZONTAL, command=self.__detectorEvent)
        self.detectors.set(200)
        self.detectors.grid(row=1, column=0)

        self.angle = Tk.Scale(self.root, from_=1, to=180, label='Angle', orient=Tk.HORIZONTAL, command=self.__angleEvent)
        self.angle.set(180)
        self.angle.grid(row=1, column=1)

        self.scans = Tk.Scale(self.root, from_=1, to=180, label='Scans', orient=Tk.HORIZONTAL, command=self.__scansEvent)
        self.scans.set(180)
        self.scans.grid(row=1, column=2)

        b = Tk.Button(self.root, text="Start", command=self.__startEvent)
        b.grid(row=2, column=1)

        self.filterBox = Tk.IntVar()
        w = Tk.Checkbutton(self.root, text="Filter", variable=self.filterBox)
        w.grid(row=1, column=3)

    def start(self):
        Tk.mainloop()

    def setSubPlot(self, array, number):
        if(number < 1 or number > 5):
            raise ValueError('Plot number must be between 1 and 5')
            return
        number += 220 # requried for add_subplot function which has 2x2 subplots
        self.subPlot = self.f.add_subplot(number)
        if(number != 222):
            self.subPlot.imshow(array, cmap=plt.cm.Greys_r)
        else:
            self.subPlot.imshow(array, cmap=plt.cm.Greys_r, aspect='auto')
        self.canvas.draw()

    def button_pressed(self, e):
        if(self.getImage() is not None):
            sinogram = self.ct.sinogram_radon(self.getImage(), self.getDetectors(), self.getAngle(), self.getScans())
            if(self.filterBox.get() == 1):
                sinogram = self.ct.filter()
            reconstructed_img = self.ct.our_restore_img_bp()
            restored = reconstructed_img
            restored = rescale(restored, scale=len(self.getImage()) / float(self.getDetectors()))
            diffValue = round(ssim(self.getImage(), restored), 3)
            l = Tk.Label(self.root, text='SSIM: ' + str(diffValue*100)+"%")
            l.grid(row=2, column=2)
            diff = self.ct.get_difference()
            self.setSubPlot(sinogram, 2)
            self.setSubPlot(reconstructed_img, 3)
            self.setSubPlot(diff, 4)

    def getDetectors(self):
        return self.detectors.get()

    def getAngle(self):
        return self.angle.get()

    def getScans(self):
        return self.scans.get()

    def getImage(self):
        return self.image

    def __detectorEvent(self, value):
        return

    def __angleEvent(self, value):
        return

    def __scansEvent(self, value):
        return

    def __startEvent(self):
        self.button_pressed(self)

    def __loadFile(self):
        Tk.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        try:
            image = imread(filename, as_grey=True)
            x, y = image.shape
            if(x != y):
                tkMessageBox.showwarning("Open file", "Image must be in square shape")
            else:
                self.image = image
                self.setSubPlot(self.image, 1)
        except IOError:
            self.image = None