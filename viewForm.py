# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewForm.ui'
#
# Created: Wed Apr 27 21:45:09 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(713, 569)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 9, 696, 481))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.loadButton = QtGui.QPushButton(self.widget)
        self.loadButton.setGeometry(QtCore.QRect(9, 9, 85, 31))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.gridLayoutWidget = QtGui.QWidget(self.widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 46, 678, 221))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.reconstructionPlot = PlotWidget(self.gridLayoutWidget)
        self.reconstructionPlot.setObjectName(_fromUtf8("reconstructionPlot"))
        self.gridLayout_2.addWidget(self.reconstructionPlot, 0, 3, 1, 1)
        self.sinogramPlot = PlotWidget(self.gridLayoutWidget)
        self.sinogramPlot.setObjectName(_fromUtf8("sinogramPlot"))
        self.gridLayout_2.addWidget(self.sinogramPlot, 0, 2, 1, 1)
        self.inputPlot = PlotWidget(self.gridLayoutWidget)
        self.inputPlot.setObjectName(_fromUtf8("inputPlot"))
        self.gridLayout_2.addWidget(self.inputPlot, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(210, 300, 211, 141))
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 713, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.loadButton.setText(_translate("MainWindow", "Load", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from pyqtgraph import PlotWidget
