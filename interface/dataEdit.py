import os
import pandas as pd

import pdb

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

qtCreatorFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resource', 'dataEdit_base.ui')
Ui_dataEditDialog, QtBaseClass = uic.loadUiType( qtCreatorFile )

class DataEdit( QDialog, Ui_dataEditDialog ):
    def __init__( self, systems, parent=None):
        QDialog.__init__( self, parent )
        Ui_dataEditDialog.__init__(self, parent)
        self.setupUi( self )
        self.systems = systems
        self.systems_original = systems
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
        self.table_MTBF.setColumnCount(1)
        self.table_MTTR.setColumnCount(1)
        self.table_N.setColumnCount(1)
        self.table_M.setColumnCount(1)
        self.table_n.setColumnCount(1)
        self.table_D.setColumnCount(1)
        self.populate()      

    def populate(self):
        for i in range(len(self.systems.keys())):
            system_key     = 'system' + str(i+1)
            layout_column  = i + 2
            system_current = self.systems[system_key].variables
            # populate spin boxes
            #  can be condensed in for loop
            self.DSBox_P.setValue(system_current.at['P',    'value'])
            self.DSBox_L.setValue(system_current.at['L',    'value'])
            self.DSBox_F.setValue(system_current.at['F',    'value'])
            self.DSBox_OC.setValue(system_current.at['OC',   'value'])
            self.DSBox_EC.setValue(system_current.at['EC',   'value'])
            self.DSBox_LC.setValue(system_current.at['LC',   'value'])
            self.DSBox_PMC.setValue(system_current.at['PMC',  'value'])
            self.DSBox_OAOC.setValue(system_current.at['OAOC', 'value'])
            self.DSBox_Cr.setValue(system_current.at['Cr',   'value'])
            self.DSBox_Cs.setValue(system_current.at['Cs',  'value'])
            self.DSBox_i.setValue(system_current.at['i',   'value'])
            # populate tables
            #  can be condensed in for loop
            values_MTBF = system_current.at['MTBF_values', 'value']
            values_MTTR = system_current.at['MTTR_values', 'value']
            values_N    = system_current.at['N', 'value']
            values_M    = system_current.at['M', 'value']
            values_n    = system_current.at['n', 'value']
            values_D    = system_current.at['D', 'value']
            vars_list = ['MTBF', 'MTTR', 'N', 'M', 'n', 'D']
            self.table_MTBF.setRowCount(len(values_MTBF)+1)
            self.table_MTTR.setRowCount(len(values_MTTR)+1)
            self.table_N.setRowCount(len(values_N)+1)
            self.table_M.setRowCount(len(values_M)+1)
            self.table_n.setRowCount(len(values_n)+1)
            self.table_D.setRowCount(len(values_D)+1)
            [self.table_MTBF.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_MTBF)]
            [self.table_MTTR.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_MTTR)]
            [self.table_N.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_N)]
            [self.table_M.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_M)]
            [self.table_n.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_n)]
            [self.table_D.setItem(i, 0, QTableWidgetItem('{}'.format(val))) for i, val in enumerate(values_D)]


    def on_accept(self):
        for i in range(len(self.systems.keys())):
            system_key     = 'system' + str(i+1)
            layout_column  = i + 2
            system_current = self.systems[system_key].variables
            # load spin box values into system dataframe
            #  can be condensed in for loop
            system_current.at['P',    'value'] = self.DSBox_P.value()
            system_current.at['L',    'value'] = self.DSBox_L.value()
            system_current.at['F',    'value'] = self.DSBox_F.value()
            system_current.at['OC',   'value'] = self.DSBox_OC.value()
            system_current.at['EC',   'value'] = self.DSBox_EC.value()
            system_current.at['LC',   'value'] = self.DSBox_LC.value()
            system_current.at['PMC',  'value'] = self.DSBox_PMC.value()
            system_current.at['OAOC', 'value'] = self.DSBox_OAOC.value()
            system_current.at['Cr',   'value'] = self.DSBox_Cr.value()
            system_current.at['Cs',   'value'] = self.DSBox_Cs.value()
            system_current.at['i',    'value'] = self.DSBox_i.value()
            # load table values into system dataframe
            #  can be condensed in for loop
            system_current.at['MTBF_values', 'value']  = [float(self.table_MTBF.takeItem(i, 0).text()) for i in range(self.table_MTBF.rowCount()-1)]
            system_current.at['MTTR_values', 'value']  = [float(self.table_MTTR.takeItem(i, 0).text()) for i in range(self.table_MTTR.rowCount()-1)]
            system_current.at['N',    'value'] = [int(self.table_N.takeItem(i, 0).text()) for i in range(self.table_N.rowCount()-1)]
            system_current.at['M',    'value'] = [int(self.table_M.takeItem(i, 0).text()) for i in range(self.table_M.rowCount()-1)]
            system_current.at['n',    'value'] = [int(self.table_n.takeItem(i, 0).text()) for i in range(self.table_n.rowCount()-1)]
            system_current.at['D',    'value'] = [int(self.table_D.takeItem(i, 0).text()) for i in range(self.table_D.rowCount()-1)]

            self.systems[system_key].variables = system_current

    def on_reject(self):
        self.systems = self.systems_original

    @staticmethod
    def editData(systems, parent=None):
        dialog = DataEdit( systems, parent )
        affirmative = dialog.exec_()
        try:
            if affirmative:
                status = 'Changes saved successfully.'
            else:
                status = 'Nothing changed.'
            return dialog.systems, status
        except Exception as e:
            print e
            return systems, 'Something\'s not quite right...'