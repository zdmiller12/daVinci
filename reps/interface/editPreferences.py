import os
import pandas as pd

import installer as INT

from easysettings import EasySettings
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# qtCreatorFile = os.path.join('.', 'resource', 'editPreferences.ui')
qtCreatorFile = INT.resource_path(os.path.join('.', 'resource', 'editPreferences.ui'))
Ui_editPreferencesDialog, QtBaseClass = uic.loadUiType( qtCreatorFile )

class EditPreferences( QDialog, Ui_editPreferencesDialog ):
    def __init__(self, daVinci, parent=None):
        QDialog.__init__(self, parent)
        Ui_editPreferencesDialog.__init__(self)
        self.setupUi(self)
        self.PP = daVinci.preferences_plotting
        self.preferences_original = daVinci.preferences_plotting
        self.buttonBox.clicked.connect(self.handle_button)
        self.populate()

    def populate(self):
        self.checkBox_gridVisibility.setChecked(self.PP.get('gridVisibility'))
        self.checkBox_horizDataLineVisibility.setChecked(self.PP.get('horizDataLineVisibility'))
        self.checkBox_vertDataLineVisibility.setChecked(self.PP.get('vertDataLineVisibility'))
        self.comboBox_annotationSize.setCurrentText(self.PP.get('annotationSize'))
        self.comboBox_axesLabelSize.setCurrentText(self.PP.get('axesLabelSize'))
        self.comboBox_fontStyle.setCurrentText(self.PP.get('fontStyle'))
        self.comboBox_gridDensity.setCurrentText(self.PP.get('gridDensity'))
        self.comboBox_gridDirection.setCurrentText(self.PP.get('gridDirection'))
        self.comboBox_markerShape.setCurrentText(self.PP.get('markerShape'))
        self.comboBox_sizeTitle.setCurrentText(self.PP.get('sizeTitle'))
        self.comboBox_tickPlacement.setCurrentText(self.PP.get('tickPlacement'))
        self.comboBox_vertDataLineColor.setCurrentText(self.PP.get('vertDataLineColor'))
        self.doubleSpinBox_annotationBuffer.setValue(self.PP.get('annotationBuffer'))
        self.doubleSpinBox_bufferXAxis.setValue(self.PP.get('bufferXAxis'))
        self.doubleSpinBox_bufferYAxis.setValue(self.PP.get('bufferYAxis'))
        self.doubleSpinBox_markerTransparency.setValue(self.PP.get('markerTransparency'))
        self.doubleSpinBox_subplotAdjust.setValue(self.PP.get('subplotAdjust'))
        self.doubleSpinBox_yAxesSeparation.setValue(self.PP.get('yAxesSeparation'))
        self.lineEdit_plotTitle.clear()
        self.lineEdit_plotTitle.insert(self.PP.get('plotTitle'))
        self.lineEdit_xLabel.clear()
        self.lineEdit_xLabel.insert(self.PP.get('xLabel'))
        self.lineEdit_yLabelInner.clear()
        self.lineEdit_yLabelInner.insert(self.PP.get('yLabelInner'))
        self.lineEdit_yLabelMiddle.clear()
        self.lineEdit_yLabelMiddle.insert(self.PP.get('yLabelMiddle'))
        self.lineEdit_yLabelOuter.clear()
        self.lineEdit_yLabelOuter.insert(self.PP.get('yLabelOuter'))
        self.spinBox_markerSize.setValue(self.PP.get('markerSize'))
        self.spinBox_tickLength.setValue(self.PP.get('tickLength'))
        self.spinBox_tickWidth.setValue(self.PP.get('tickWidth'))

    def apply_changes(self):
        self.PP.set('gridVisibility', self.checkBox_gridVisibility.isChecked())
        self.PP.set('horizDataLineVisibility', self.checkBox_horizDataLineVisibility.isChecked())
        self.PP.set('vertDataLineVisibility', self.checkBox_vertDataLineVisibility.isChecked())
        self.PP.set('annotationSize', self.comboBox_annotationSize.currentText())
        self.PP.set('axesLabelSize', self.comboBox_axesLabelSize.currentText())
        self.PP.set('fontStyle', self.comboBox_fontStyle.currentText())
        self.PP.set('gridDensity', self.comboBox_gridDensity.currentText())
        self.PP.set('gridDirection', self.comboBox_gridDirection.currentText())
        self.PP.set('markerShape', self.comboBox_markerShape.currentText())
        self.PP.set('sizeTitle', self.comboBox_sizeTitle.currentText())
        self.PP.set('tickPlacement', self.comboBox_tickPlacement.currentText())
        self.PP.set('vertDataLineColor', self.comboBox_vertDataLineColor.currentText())
        self.PP.set('annotationBuffer', self.doubleSpinBox_annotationBuffer.value())
        self.PP.set('bufferXAxis', self.doubleSpinBox_bufferXAxis.value())
        self.PP.set('bufferYAxis', self.doubleSpinBox_bufferYAxis.value())
        self.PP.set('markerTransparency', self.doubleSpinBox_markerTransparency.value())
        self.PP.set('subplotAdjust', self.doubleSpinBox_subplotAdjust.value())
        self.PP.set('yAxesSeparation', self.doubleSpinBox_yAxesSeparation.value())
        self.PP.set('plotTitle', self.lineEdit_plotTitle.text())
        self.PP.set('xLabel', self.lineEdit_xLabel.text())
        self.PP.set('yLabelInner', self.lineEdit_yLabelInner.text())
        self.PP.set('yLabelMiddle', self.lineEdit_yLabelMiddle.text())
        self.PP.set('yLabelOuter', self.lineEdit_yLabelOuter.text())
        self.PP.set('markerSize', self.spinBox_markerSize.value())
        self.PP.set('tickLength', self.spinBox_tickLength.value())
        self.PP.set('tickWidth', self.spinBox_tickWidth.value())
    	
    def change_nothing(self):
        self.PP = self.preferences_original

    def handle_button(self, button):
        global daVinci_main
        sb = self.buttonBox.standardButton(button)
        if sb == QDialogButtonBox.Apply:
            self.apply_changes()
            daVinci_main.dataPlot_SLOT()
        elif sb == QDialogButtonBox.RestoreDefaults:
            self.restore_defaults()

    def restore_defaults(self):
        defaults = EasySettings(os.path.join(os.getcwd(), 'parameters', 'default','preferences_plotting-default.conf'))
        for setting in defaults.list_settings():
            self.PP.set(setting[0], setting[1])
        self.populate()
            
    @staticmethod
    def editPreferences(daVinci, parent=None):
        dialog = EditPreferences(daVinci, parent)
        affirmative = dialog.exec_()
        try:
            if affirmative:
                dialog.apply_changes()
                status = 'Successfully updated plotting preferences.'
            else:
                dialog.change_nothing()
                status = 'Nothing changed.'
            return dialog.PP, status
        except Exception as e:
            return preferences, 'Something\'s not right...'
