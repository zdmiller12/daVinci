import os
import pandas as pd

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ContentHandler:

    def get_chapter(self):
        """
        Returns
        -------
        int
            SEA chapter number (international edition).
        """
        return self.spinBox_chapter.value()


    def get_problem(self):
        """
        Returns
        -------
        int
            SEA problem number (international edition).
        """
        return self.spinBox_problem.value()

    def get_version(self):
        """
        Returns
        -------
        str
            'SEA' or 'STEA'
        """
        return self.comboBox_which.currentText()
    
        