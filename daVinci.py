"""
Created by Zack Miller
Version 2019.11.10

Contact: zdmiller12@gmail.com
""" 

import os, sys

from reps import systemInfo as INFO
from reps.include.mainClassDataFrame import MainClassDataFrame as MCDF
from reps.include.optimization import Optimization as OPT
from reps.interface.dataEdit import DataEdit as DE
from reps.interface.editPreferences import EditPreferences as PREF
from reps.interface.userActions import UserActions as ACT
from reps.output import feedback as FEED
from reps.output import resultsPlot as PLOT
from reps.output import resultsTable as TABLE

from easysettings import EasySettings

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


qtCreatorFile = INFO.resource_path(os.path.join('.', 'reps', 'resource', 'mainWindow.ui'))
Ui_MainWindow, QtBaseClass = uic.loadUiType( qtCreatorFile )

class daVinci( QMainWindow, Ui_MainWindow ):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        # Preferences
        self.preferences_plotting = EasySettings(os.path.join(os.getcwd(), 'reps', 'parameters', 'default', 'preferences_plotting-default.conf'))
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
        self.pushButton_plotPreferences.clicked.connect(self.editPreferences_SLOT)
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

    def dataEdit_SLOT(self):
        self.statusbar.showMessage('Editing data...')
        self.systems, status = DE.editData(self.systems)
        self.statusbar.showMessage(status)

    def calculateResults_SLOT(self):
        self.statusbar.showMessage('Calculating all results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            valid, culprits = system_current.return_validity()
            if not valid:
                msg = 'System data is not valid.  Variable(s) {} cannot be 0'.format(culprits)
                FEED.handle_invalid_system_data(self, msg)
            else:
                OPT(system_current)
                TABLE.table_results(self, system_current)
                TABLE.check_all_iters(self)
                try:
                    PLOT.plot_results(self, system_current)
                except Exception as e:
                    raise
                self.statusbar.showMessage('See table and plot for results.')


    def dataPlot_SLOT(self):
        self.statusbar.showMessage('Plotting selected results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            PLOT.plot_results(self, system_current)

        self.statusbar.clearMessage()

    def dataTable_SLOT(self):
        self.statusbar.showMessage('Calculating tabular results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            OPT(system_current)
            TABLE.table_results(self, system_current)

        self.statusbar.clearMessage()

    def editPreferences_SLOT(self):
        self.statusbar.showMessage('Editing preferences...')
        self.preferences_plotting, status = PREF.editPreferences(self)
        self.statusbar.showMessage(status)

    def cellChecker_SLOT(self, checked):
        if checked:
            TABLE.check_all_iters(self)
        else:
            TABLE.uncheck_all_iters(self)

    def cellSelection_SLOT(self, item):
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
    daVinci_main = daVinci()

    # minimized
    # gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    # gallery.resize( 0.6*w, 0.6*h )

    # 
    daVinci_main.show()
    app.exec()
    #sys.exit( app.exec_() )
