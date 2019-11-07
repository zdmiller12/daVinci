import os

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

qtCreatorFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resource', 'userAction.ui')
Ui_userActionDialog, QtBaseClass = uic.loadUiType( qtCreatorFile )

class UserActions( QDialog, Ui_userActionDialog ):
    def __init__( self, prompt, prompt_details, parent=None):
        QDialog.__init__( self, parent )
        Ui_userActionDialog.__init__(self, parent)
        self.setupUi( self )

        full_prompt = 'Are you sure you would like to {}?\n\n{}'.format(prompt, prompt_details)
        self.label_userPrompt.setText(full_prompt)


    @staticmethod
    def newSystem(self, parent=None):
        prompt_type =  'create a new system'
        details  = 'Unsaved changes will be sent to space.'
        dialog   = UserActions( prompt_type, details, parent )
        affirmative = dialog.exec_()
        if affirmative:
            try:
                self.systems['system1'].update_variables(self.systems['system1'].default_system_filePath)
                return 'Successfully created new system.'
            except Exception as e:
                print e
                return 'Failed to create new system \n{}'.format(e)
        else:
            return 'Nothing changed.'


    @staticmethod
    def loadSystem(self, parent=None):
        options  = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open System File", os.path.join(os.getcwd(), 'parameters', 'user', 'systems', 'examples'), 'Pickled DataFrames (*.pkl)')
        if fileName:
            try:
                self.systems['system1'].update_variables(fileName)
                return 'Successfully loaded {}'.format(fileName)
            except Exception as e:
                print e
                return None, 'Failed to load {}'.format(fileName)


    @staticmethod
    def saveSystem(self, parent=None):
        fileName, _ = QFileDialog.getSaveFileName(self, "Pickle System File for Later", os.path.join(os.getcwd(), 'parameters', 'user', 'systems'), '*.pkl')
        if fileName:
            if '.' in fileName and fileName[-4:] != '.pkl':
                fileName = fileName.replace(fileName[fileName.find('.'):], '.pkl')
            elif '.' not in fileName:
                fileName = '{}.pkl'.format(fileName)
            try:
                self.systems['system1'].save_dataFrame(fileName)
                return 'Successfully saved current system as {}'.format(fileName)
            except Exception as e:
                print e
                return None, 'Failed to load {}'.format(fileName)


    @staticmethod
    def quit(self, parent=None):
        prompt_type = 'quit'
        details = 'Unsaved changes will be buried underneath the ocean.'
        dialog  = UserActions( prompt_type, details, parent )
        affirmative  = dialog.exec_()
        if affirmative:
            sys.exit(1)
        else:
            return 'Nothing changed.'
