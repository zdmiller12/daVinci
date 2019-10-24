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

import attributeHandler as aH
import include.basicFunctions as bF
from mainClassDataFrame import mainClassDataFrame as mC
from interface.dataEdit import DataEdit as DE
# from parameters.userDefined import userDefined as uD

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
        self.systems = {}
        self.systems['system1'] = mC('system1')
        ###
        ##
        #    SIGNALS
        self.pushButton_dataEdit.clicked.connect(self.pushButton_dataEdit_SLOT)
        self.pushButton_dataPlot.clicked.connect(self.pushButton_dataPlot_SLOT)
        #
        ##
        ###
    #######
    ###
    ##
    #    SLOTS
    def pushButton_dataEdit_SLOT( self ):
        self.statusbar.showMessage('Editing data...')
        self.systems = DE.editData(self.systems)
        self.statusbar.clearMessage()
        print self.systems['system1'].variables

    def pushButton_dataPlot_SLOT( self ):
        self.statusbar.showMessage('Calculating results...')
        for i in range(len(self.systems.keys())):
            system_key = 'system' + str(i+1)
            system_current = self.systems[system_key]
            self.setup_optimizer(system_current)
            self.table_results(system_current)

        self.statusbar.clearMessage()
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

    def plot_results( self ):
        print self.simulated_values.loc[['n','N','M','TC'],:]
        plot_type = 'multiple_axes'
        x_variables = ['AELCC']
        y_variables = ['MTBF_average', 'P0', 'PFC']
        x_values    = self.simulated_values.loc[x_variables,:].values.tolist()
        y_values    = self.simulated_values.loc[y_variables,:].values.tolist()
        gP.createPlot( x_values, y_values  )

    def table_results( self, system_current ):
        table = self.table_results_system1
        column_count = 5
        table.setRowCount(9)
        table.setColumnCount(column_count)

        header = self.table_results_system1.horizontalHeader()
        [header.setSectionResizeMode(i, QHeaderView.ResizeToContents) for i in range(column_count)]
         
        items_per_item_in_first_column = len(system_current.simulation_values['N'])
        headers = ['Retirement Age: n', 'Number of Units: N', 
                  'Repair Channels=2', 'Repair Channels=3', 'Repair Channels=4']

        table.setHorizontalHeaderLabels(headers)
        # set data
        for k in range(len(system_current.simulation_values['n'])):
            first_col_step = k*items_per_item_in_first_column
            val_n = system_current.simulation_values['n'][k]
            table.setItem(first_col_step, 0, QTableWidgetItem('{}'.format(val_n)))
            for i in range(len(system_current.simulation_values['N'])):
                val_N = system_current.simulation_values['N'][i]
                table.setItem(first_col_step+i, 1, QTableWidgetItem('{}'.format(val_N)))
                for j in range(len(system_current.simulation_values['M'])):
                    val_M = system_current.simulation_values['M'][j]
                    indy     = ((system_current.simulated_values.loc['n'] == val_n) &
                                (system_current.simulated_values.loc['N'] == val_N) & 
                                (system_current.simulated_values.loc['M'] == val_M) )
                    table_value = system_current.simulated_values.loc['TC', indy].tolist()[0]
                    table.setItem(first_col_step+i, 2+j, QTableWidgetItem('{:.0f}'.format(table_value)))

        
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
    gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    gallery.resize( 0.6*w, 0.6*h )
    gallery.show()
    sys.exit( app.exec_() )