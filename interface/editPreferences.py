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
        self.preferences = preferences
        self.preferences_original = preferences


    def on_accept(self):
    	self.preferences = self.preferences_original
        

    def on_reject(self):
        self.preferences = self.preferences_original

    @staticmethod
    def editPreferences(preferences, parent=None):
        dialog   = EditPreferences( preferences, parent )
        result   = dialog.exec_()
        return dialog.preferences