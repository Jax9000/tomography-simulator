import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot
import pyqtgraph as pg
import numpy as np

import viewForm as form
from skimage.io import imread
from skimage import data_dir

def something(var):
    print "xD"

@pyqtSlot()
def selectFile():
    print QFileDialog.getOpenFileName()

def showSampleWindow():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = form.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.loadButton.clicked.connect(selectFile)
    image = imread(data_dir + "/phantom.png", as_grey=True)
    # print image
    # print np.random.normal(size=100)
    pixmap = QPixmap(image)
    ui.label.setPixmap(pixmap)

    # ui.graphicsView.
    MainWindow.show()
    sys.exit(app.exec_())