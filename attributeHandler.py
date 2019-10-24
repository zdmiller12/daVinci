import pdb

import numpy as np
import pandas as pd

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def get_designDependParams_tables( parent ):
    tables = []
    layout = parent.layout_designDependParams
    items = [layout.itemAt(i).widget() for i in range(layout.count())]
    for item in items:
        if type(item) is QTableWidget:
            tables.append(item.objectName())
        else:
            continue
    return tables


def draw_tables( parent ):
    systems = sorted(parent.candidateSystems.items(), key= lambda kv: kv[0])
    show_N  = parent.spinBox_candidateSystem_N.value()

    for table in get_designDependParams_tables( parent ):
        table_variable = str(table)[6:]
        current_table  = getattr(parent, str(table))
        current_table.setRowCount(show_N)
        for index, system in enumerate(systems):
            if index >= show_N: break
            current_name       = system[0]
            current_df         = system[1]
            current_value      = current_df.at[table_variable, 'value']
            current_item_value = QTableWidgetItem('{}'.format(current_value))
            current_item_name  = QTableWidgetItem('{}'.format(current_name))
            current_table.setItem(index, 0, current_item_name)
            current_table.setItem(index, 1, current_item_value)
