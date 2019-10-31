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
import itertools
import numpy as np
import pandas as pd

from include import basicFunctions as bF
from include.mainClassDataFrame import mainClassDataFrame as mC
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
        self.systems['system1'] = mC('system1')
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
        self.decision = ACT.newSystem(self)
        print self.decision
        self.statusbar.clearMessage()

    def loadSystem_SLOT( self ):
        self.statusbar.showMessage('Loading system(s)...')
        self.decision = ACT.loadSystem(self)
        print self.decision
        self.statusbar.clearMessage()

    def saveSystem_SLOT( self ):
        self.statusbar.showMessage('Saving current system(s)...')
        self.decision = ACT.saveSystem(self)
        print self.decision
        self.statusbar.clearMessage()

    def quit_SLOT( self ):
        self.statusbar.showMessage('Quitting TOPS...')
        self.decision = ACT.quit(self)
        print self.decision
        self.statusbar.clearMessage()

    def dataEdit_SLOT( self ):
        self.statusbar.showMessage('Editing data...')
        self.systems = DE.editData(self.systems)
        self.statusbar.clearMessage()

    def calculateResults_SLOT( self ):
        self.statusbar.showMessage('Calculating all results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            self.setup_optimizer(system_current)
            self.table_results(system_current)
            TABLE.check_all_iters(self)
            self.plot_results(system_current)

        self.statusbar.clearMessage()

    def dataPlot_SLOT( self ):
        self.statusbar.showMessage('Plotting selected results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            self.plot_results(system_current)

        self.statusbar.clearMessage()

    def dataTable_SLOT( self ):
        self.statusbar.showMessage('Calculating tabular results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            self.setup_optimizer(system_current)
            self.table_results(system_current)

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

    def setup_optimizer( self, system_current ):
        system_current.clear_simulated_values()
        self.create_simulation_array(system_current)
        for sim_vals in system_current.simulation_array:
            self.column_header = 'iter_' + str(system_current.iterations_completed() + 1)
            system_current.create_new_variable_set(self.column_header)
            system_current.variable_set.loc[system_current.variables_to_optimize, self.column_header] = sim_vals
            total_cost = self.calculate_total_cost(system_current)
            within_constraints = self.check_constraints(system_current)
            if within_constraints:
                system_current.simulated_values = system_current.simulated_values.join(system_current.variable_set)
            else:
                continue
        
    def create_simulation_array( self, system_current ):
        opt_variables = system_current.variables.index[system_current.variables['optimize']].tolist()
        simulation_values = {}
        for var in opt_variables:
            minimum = system_current.variables.at[var, 'bound_low']
            maximum = system_current.variables.at[var, 'bound_high']
            increment = system_current.variables.at[var, 'sim_increment']
            sim_list = [i for i in range(minimum, maximum+increment, increment)]
            simulation_values[var] = sim_list

        variables_to_optimize = simulation_values.keys()
        simulation_array = list(itertools.product(*simulation_values.values()))
        system_current.set_variables_to_optimize(variables_to_optimize)
        system_current.set_simulation_values(simulation_values)
        system_current.set_simulation_array(simulation_array)

    def calculate_total_cost( self, system_current ):
        self.counter = 0
        while np.isnan(system_current.variable_set.at['TC', self.column_header]) and self.counter < 5:
            self.calculate_new_variables(system_current)
            self.counter += 1

    def calculate_new_variables( self, system_current ):
        for equation_name, equation_variables in system_current.variables_per_equation.items():
            have_NaN = False
            send_variables = []
            var = equation_name[5:]
            check_variables = system_current.variable_set.loc[equation_variables, self.column_header].values
            for variable in check_variables:
                if np.any(np.isnan(variable)): 
                    have_NaN = True
                    break
                else: send_variables.append(variable)
            if have_NaN: continue
            if np.any(np.isnan(system_current.variable_set.at[var, self.column_header])):
                fun = getattr(bF, equation_name)
                system_current.variable_set.at[var, self.column_header] = fun(*send_variables)
                # print('CALCULATED {} as {}'.format(var, system_current.variable_set.at[var, self.column_header]))
                self.counter = 0

    def check_constraints( self, system_current ):
        within_constraints = True
        for con in system_current.return_constrained_variables():
            if not np.any(np.isnan(system_current.variables.at[con, 'constraint_low'])) and (system_current.variable_set.at[con, self.column_header] < system_current.variables.at[con, 'constraint_low']):
                within_constraints = False
                print system_current.variable_set[self.column_header]
                print 'variable {} breaks low constraint at {}'.format(con, system_current.variable_set.at[con, self.column_header])
                break
            if not np.any(np.isnan(system_current.variables.at[con, 'constraint_high'])) and (system_current.variable_set.at[con, self.column_header] > system_current.variables.at[con, 'constraint_high']):
                within_constraints = False
                print system_current.variable_set[self.column_header]
                print 'variable {} breaks high constraint at {}'.format(con, system_current.variable_set.at[con, self.column_header])
                break

        if within_constraints:
            return True
        else:
            return False

    def plot_results( self, system_current ):
        PLOT.plot( self, system_current )
        

    def table_results( self, system_current ):
        TABLE.table( self, system_current )


        
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