from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel, QTableWidgetItem


def handle_invalid_system_data(self, message):
    invalid_msg_label = QLabel(message)
    font = invalid_msg_label.font()
    font.setPointSize(24)
    font.setBold(True)
    invalid_msg_label.setAlignment(Qt.AlignCenter)
    invalid_msg_label.setWordWrap(True)
    invalid_msg_label.setFont(font)
    self.verticalLayout_resultsPlot.addWidget(invalid_msg_label)
    self.tableWidget_resultsTable.setRowCount(1)
    self.tableWidget_resultsTable.setColumnCount(1)
    table_msg = QTableWidgetItem(message)
    table_msg.setFont(font)
    self.tableWidget_resultsTable.setItem(0, 0, table_msg)
    self.tableWidget_resultsTable.resizeColumnsToContents()
    self.statusbar.showMessage(message)