from PyQt5 import QtCore
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem

from interface.editPreferences import EditPreferences as PREF


def table( self, system_current ):
    table = self.tableWidget_resultsTable
    column_count = 5
    table.setRowCount(9)
    table.setColumnCount(column_count)

    header = self.tableWidget_resultsTable.horizontalHeader()
    [header.setSectionResizeMode(i, QHeaderView.ResizeToContents) for i in range(column_count)]
     
    items_per_item_in_first_column = len(system_current.simulation_values['N'])
    headers = ['Retirement Age: n', 'Number of Units: N', 
              'Repair Channels=2', 'Repair Channels=3', 'Repair Channels=4']

    table.setHorizontalHeaderLabels(headers)

    # set data
    for k in range(len(system_current.simulation_values['n'])):
        first_col_step = k*items_per_item_in_first_column
        val_n = system_current.simulation_values['n'][k]
        header_item = QTableWidgetItem('{}'.format(val_n))
        header_item.setWhatsThis('header')
        table.setItem(first_col_step, 0, header_item)
        for i in range(len(system_current.simulation_values['N'])):
            val_N = system_current.simulation_values['N'][i]
            header_item = QTableWidgetItem('{}'.format(val_N))
            header_item.setWhatsThis('header')
            table.setItem(first_col_step+i, 1, header_item)
            for j in range(len(system_current.simulation_values['M'])):
                val_M = system_current.simulation_values['M'][j]
                indy  = ((system_current.simulated_values.loc['n'] == val_n) &
                         (system_current.simulated_values.loc['N'] == val_N) & 
                         (system_current.simulated_values.loc['M'] == val_M) )
                table_value = system_current.simulated_values.loc['TC', indy].tolist()[0]
                iter_index  = indy[indy].index.tolist()[0]
                new_item = QTableWidgetItem('{:.0f}'.format(table_value))
                new_item.setWhatsThis('{}'.format(iter_index))
                table.setItem(first_col_step+i, 2+j, new_item)

def handle_table_click( self, item ):
    if item is None or item.whatsThis() == 'header':
        return None
    
    if not item.checkState():
        item.setCheckState(QtCore.Qt.Checked)
    else:
        item.setCheckState(QtCore.Qt.Unchecked)

def check_all_iters( self ):
    table = self.tableWidget_resultsTable
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is None or item.whatsThis() == 'header':
                continue
            item.setCheckState(QtCore.Qt.Checked)


def uncheck_all_iters( self ):
    table = self.tableWidget_resultsTable
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is None or item.whatsThis() == 'header':
                continue
            item.setCheckState(QtCore.Qt.Unchecked)

def get_checked_iters( self ):
    checked_iters = []
    table = self.tableWidget_resultsTable
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)

            if item is None or item.whatsThis() == 'header':
                continue

            if item.checkState():
                checked_iters.append(item.whatsThis())

    return checked_iters