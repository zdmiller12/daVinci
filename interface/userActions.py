import os
import pandas as pd

from include.mainClassDataFrame import mainClassDataFrame as mC

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
        options  = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open System File", os.path.join(os.getcwd(), 'parameters', 'user'), 'Pickled DataFrames (*.pkl)')
        if fileName:
            try:
                mC.update_variables(self.systems['system1'], fileName)
                return 'Successfully loaded {}'.format(fileName)
            except Exception as e:
                print e
                return None, 'Failed to load {}'.format(fileName)


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