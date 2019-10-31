#!/usr/bin/env python


#############################################################################
##
## Decision Evaluation Display
##
## Zachary Miller
## October 2018
## zdmiller12@gmail.com
##
#############################################################################

import pdb
import os, sys

from include.mainClassDataFrame import mainClassDataFrame as MCDF
from include.optimization import Optimization as OPT
from interface.dataEdit import DataEdit as DE
from interface.editPreferences import EditPreferences as PREF
from interface.userActions import UserActions as ACT
from output import resultsPlot as PLOT
from output import resultsTable as TABLE

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

qtCreatorFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource', 'mainWindow.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType( qtCreatorFile )

class daVinci( QMainWindow, Ui_MainWindow ):

    def __init__( self, parent=None ):
        QMainWindow.__init__( self )
        Ui_MainWindow.__init__( self )
        self.setupUi( self )
        # Preferences
        self.showMaximized()
        self.preferences = 4
        # System(s) Loading
        self.systems = {}
        self.systems['system1'] = MCDF('system1')
        #
        ##
        ###
        ##    SIGNALS
        #
        # File
        self.actionFile_newSystem.triggered.connect(self.newSystem_SLOT)
        self.actionFile_loadSystem.triggered.connect(self.loadSystem_SLOT)
        self.actionFile_saveSystem.triggered.connect(self.saveSystem_SLOT)
        self.actionFile_quit.triggered.connect(self.quit_SLOT)
        # Edit
        self.actionEdit_dataEdit.triggered.connect(self.dataEdit_SLOT)
        self.actionEdit_calculateResults.triggered.connect(self.calculateResults_SLOT)
        self.actionEdit_refreshTable.triggered.connect(self.dataTable_SLOT)
        self.actionEdit_refreshPlot.triggered.connect(self.dataPlot_SLOT)
        self.actionEdit_editPreferences.triggered.connect(self.editPreferences_SLOT)
        # Buttons
        self.pushButton_dataEdit.clicked.connect(self.dataEdit_SLOT)
        self.pushButton_calculateResults.clicked.connect(self.calculateResults_SLOT)
        self.pushButton_refreshTable.clicked.connect(self.dataTable_SLOT)
        self.pushButton_refreshPlot.clicked.connect(self.dataPlot_SLOT)
        self.pushButton_cellChecker.clicked.connect(self.cellChecker_SLOT)
        self.pushButton_editPreferences.clicked.connect(self.editPreferences_SLOT)
        # Results
        self.tableWidget_resultsTable.itemClicked.connect(self.cellSelection_SLOT)
        #
        ##
        ###
    #######
    ###
    ##    SLOTS
    #
    def newSystem_SLOT( self ):
        self.statusbar.showMessage('Creating new system...')
        status = ACT.newSystem(self)
        self.statusbar.showMessage(status)

    def loadSystem_SLOT( self ):
        self.statusbar.showMessage('Loading system...')
        status = ACT.loadSystem(self)
        self.statusbar.showMessage(status)

    def saveSystem_SLOT( self ):
        self.statusbar.showMessage('Saving current system...')
        status = ACT.saveSystem(self)
        self.statusbar.showMessage(status)

    def quit_SLOT( self ):
        self.statusbar.showMessage('Quitting TOPS...')
        status = ACT.quit(self)
        self.statusbar.showMessage(status)

    def dataEdit_SLOT( self ):
        self.statusbar.showMessage('Editing data...')
        self.systems, status = DE.editData(self.systems)
        self.statusbar.showMessage(status)

    def calculateResults_SLOT( self ):
        self.statusbar.showMessage('Calculating all results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            OPT(system_current)
            TABLE.table_results(self, system_current)
            TABLE.check_all_iters(self)
            PLOT.plot_results( self, system_current)

        self.statusbar.clearMessage()

    def dataPlot_SLOT( self ):
        self.statusbar.showMessage('Plotting selected results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            PLOT.plot_results(self, system_current)

        self.statusbar.clearMessage()

    def dataTable_SLOT( self ):
        self.statusbar.showMessage('Calculating tabular results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            OPT(system_current)
            TABLE.table_results(self, system_current)

        self.statusbar.clearMessage()

    def editPreferences_SLOT( self ):
        self.statusbar.showMessage('Editing preferences...')
        self.preferences = PREF.editPreferences(self.preferences)
        self.statusbar.clearMessage()

    def cellChecker_SLOT( self, checked ):
        if checked:
            TABLE.check_all_iters(self)
        else:
            TABLE.uncheck_all_iters(self)

    def cellSelection_SLOT( self, item ):
        TABLE.handle_table_click(self, item)
    #
    ##
    ###

        
if __name__ == '__main__':

    # # for windows screen
    # from win32api import GetSystemMetrics
    # print("Width =", GetSystemMetrics(0))
    # print("Height =", GetSystemMetrics(1))

    # this may not work with windows/mac
    app     = QApplication( sys.argv )
    screen  = app.desktop().screenGeometry()
    w, h    = screen.width(), screen.height()
    gallery = daVinci()

    # minimized
    # gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    # gallery.resize( 0.6*w, 0.6*h )

    # 
    gallery.show()
    sys.exit( app.exec_() )