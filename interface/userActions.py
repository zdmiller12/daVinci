import os
import pandas as pd

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

qtCreatorFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resource', 'userAction.ui')
Ui_userActionDialog, QtBaseClass = uic.loadUiType( qtCreatorFile )

class UserActions( QDialog, Ui_userActionDialog ):
    def __init__( self, prompt, parent=None):
        QDialog.__init__( self, parent )
        Ui_userActionDialog.__init__(self, parent)
        self.setupUi( self )
        self.decision = 'no'

        full_prompt = 'Are you sure you would like to {}?'.format(prompt)
        self.label_userPrompt.setText(full_prompt)

        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)


    def on_accept(self):
        self.decision = 'yes'
        
    def on_reject(self):
        self.decision = 'no'

    @staticmethod
    def newSystem( self, parent=None ):
        prompt_type =  'create a new system'
        dialog   = UserActions( prompt_type, parent )
        result   = dialog.exec_()
        return dialog.decision

    @staticmethod
    def loadSystem( self, parent=None ):
        prompt_type = 'load existing system(s)'
        dialog   = UserActions( prompt_type, parent )
        result   = dialog.exec_()
        return dialog.decision
        # self.fileName = QFileDialog.getOpenFileName( self, 'Open CSV File', self.currentDirectory + os.path.sep + 'save', 'CSV Files (*.csv)')
        # convertData( self )

    @staticmethod
    def saveSystem( self, parent=None ):
        prompt_type = 'save current system(s)'
        dialog   = UserActions( prompt_type, parent )
        result   = dialog.exec_()
        return dialog.decision

    @staticmethod
    def quit( self, parent=None ):
        prompt_type = 'quit'
        dialog   = UserActions( prompt_type, parent )
        result   = dialog.exec_()
        return dialog.decision