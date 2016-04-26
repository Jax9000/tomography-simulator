import sys
from PyQt4 import QtGui

def showSampleWindow():
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    window.setGeometry(0, 0, 500, 500)
    window.setWindowTitle("Hello world");

    window.show()

    app.exec_();