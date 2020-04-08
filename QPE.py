"""
Created by Zack Miller
Version 

Contact: zdmiller12@gmail.com
""" 

import os, sys
from easysettings import EasySettings

from qpe.mainHandler import MainHandler

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


qtCreatorFile = os.path.join('.', 'qpe', 'resource', 'qpe_mainWindow.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType( qtCreatorFile )

class QPE( QMainWindow, Ui_MainWindow, MainHandler ):
    def __init__(self, parent=None):
        self.qpeDirectory = os.getcwd()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        MainHandler.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        #
        ##
        ###
        ##    SIGNALS
        #
        #
        self.comboBox_book.currentTextChanged.connect(self.dialog_update_SLOT)
        self.spinBox_chapter.valueChanged.connect(self.dialog_update_SLOT)
        self.spinBox_problem.valueChanged.connect(self.dialog_update_SLOT)
        #
        ##
        ###
    #######
    ###
    ##    SLOTS
    #
    def dialog_update_SLOT(self):
        self.update_statusbar()
        self.update_labels()
    

if __name__ == '__main__':
    # # for windows screen
    # from win32api import GetSystemMetrics
    # print("Width =", GetSystemMetrics(0))
    # print("Height =", GetSystemMetrics(1))

    # this may not work with windows/mac
    app     = QApplication( sys.argv )
    screen  = app.desktop().screenGeometry()
    w, h    = screen.width(), screen.height()
    qpe_main = QPE()

    # minimized
    # gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    # gallery.resize( 0.6*w, 0.6*h )

    # 
    qpe_main.show()
    app.exec()
    #sys.exit( app.exec_() )