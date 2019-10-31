import os
import pandas as pd

import pdb

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

qtCreatorFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resource', 'editPreferences.ui')
Ui_editPreferencesDialog, QtBaseClass = uic.loadUiType( qtCreatorFile )

class EditPreferences( QDialog, Ui_editPreferencesDialog ):
    def __init__( self, preferences, parent=None):
        QDialog.__init__( self, parent )
        Ui_editPreferencesDialog.__init__(self, parent)
        self.setupUi( self )
        self.PP = preferences
        self.preferences_original = preferences
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
        self.populate()

    def populate(self):
        self.doubleSpinBox_bufferXAxis.setValue(self.PP.get('buffer_x_axis'))
        self.spinBox_tickLength.setValue(self.PP.get('tick_length'))
        self.spinBox_markerSize.setValue(self.PP.get('marker_size'))
        self.comboBox_sizeTitle.setCurrentText(self.PP.get('size_title'))

    def on_accept(self):
        self.PP.set('buffer_x_axis', self.doubleSpinBox_bufferXAxis.value())
        self.PP.set('tick_length', self.spinBox_tickLength.value())
        self.PP.set('marker_size', self.spinBox_markerSize.value())
        self.PP.set('size_title', self.comboBox_sizeTitle.currentText())
    	

    def on_reject(self):
        self.PP = self.preferences_original

    @staticmethod
    def editPreferences(preferences, parent=None):
        dialog   = EditPreferences( preferences, parent )
        affirmative = dialog.exec_()
        try:
            if affirmative:
                status = 'Successfully updated plotting preferences.'
            else:
                status = 'Nothing changed.'
            return dialog.PP, status
        except Exception as e:
            return preferences, 'Something\'s not right...'