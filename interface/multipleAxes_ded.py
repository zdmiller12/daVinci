#!/usr/bin/env python


#############################################################################
##
## Decision Evaluation Display
##
## Zachary Miller
## October 2018
## zdmiller12@gmail.com
##
#############################################################################

from PyQt5 import QtCore
from PyQt5.QtCore import (QDateTime, Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, 
        QLineEdit,QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy, QSlider, 
        QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QVBoxLayout, 
        QWidget)
from PyQt5.QtGui import (QCursor, QValidator, QDoubleValidator)


class DecisionEvaluationDisplay( QDialog ):

    def __init__( self, parent=None ):
        super( DecisionEvaluationDisplay, self ).__init__( parent )

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems( QStyleFactory.keys() )
        styleComboBox.setCursor( QCursor( Qt.PointingHandCursor ) )
        styleLabel = QLabel( '&Style:' )
        styleLabel.setBuddy( styleComboBox )

        self.useStylePaletteCheckBox = QCheckBox( '&Use Standard Palette' )
        self.useStylePaletteCheckBox.setChecked( True )
        self.useStylePaletteCheckBox.setCursor( QCursor( Qt.PointingHandCursor ) )

        self.userOptionN   = 1
        self.userCriteriaN = 0

        self.runOnce()
        self.loadData()
        self.createFormatGroupBox()
        self.createInputGroupBox()
        self.createEnterCriteriaGroupBox()
        self.createModifyCriteriaGroupBox()
        self.createUpdatePlotGroupBox()

        styleComboBox.activated[str].connect( self.changeStyle )
        self.useStylePaletteCheckBox.toggled.connect( self.changePalette )

        topLayout = QHBoxLayout()
        topLayout.addWidget( styleLabel )
        topLayout.addWidget( styleComboBox )
        topLayout.addStretch( 1 )
        topLayout.addWidget( self.useStylePaletteCheckBox )

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout( topLayout, 0, 0, 1, 2 )
        self.mainLayout.addWidget( self.formatGroupBox, 1, 0, 1, 1 )
        self.mainLayout.addWidget( self.enterCriteriaGroupBox,  1, 1, 1, 1 )
        self.mainLayout.addWidget( self.modifyCriteriaGroupBox, 2, 0, 1, 2 )
        self.mainLayout.addWidget( self.inputGroupBox, 3, 0, 1, 2 )
        self.mainLayout.addWidget( self.updatePlotGroupBox, 4, 0, 1, 2)
        self.mainLayout.setRowStretch( 0, 0 )
        self.mainLayout.setRowStretch( 1, 0 )
        self.mainLayout.setRowStretch( 2, 1 )
        self.mainLayout.setRowStretch( 3, 1 )
        self.mainLayout.setRowStretch( 4, 0 )
        self.mainLayout.setColumnStretch( 0, 1 )
        self.mainLayout.setColumnStretch( 1, 1 )
        self.mainLayout.setVerticalSpacing( 10 )
        self.setLayout( self.mainLayout )

        self.setWindowTitle( 'Decision Evaluation Display Generator' )
        self.changeStyle( 'GTK+' )
        self.saveData()


    # modifies the criteria input matrix based on user input
    # rows 2 and greater in 'Input for Options to Compare' box
    def addCriteriaToData( self ):

        if str( self.userCriteriaEdit.text() ) == '':
            return

        self.saveData()
        newCriteria  = str( self.userCriteriaEdit.text() )
        self.userCriteriaEdit.clear()

        if newCriteria in self.criteriaData['criteria']:
            return
        
        self.userCriteriaN += 1
        newCriteriaTuple    = tuple( [ newCriteria ] + [ float(0) for i in range( 1+self.maxOptions ) ] ) # extra 0 for target value
        self.criteriaData   = np.append( self.criteriaData, np.array( [ newCriteriaTuple ], self.dtype ) )
        self.criteriaData   = np.sort( self.criteriaData, order='criteria' )

        self.changeInputLayout()
        self.addCriteriaComparisonItems()
        self.saveData()


    # modifies the criteria box based on user input
    # 'Comparison Items' box
    def addCriteriaComparisonItems( self ):
        self.clearLayout( self.modifyCriteriaLayout )
        self.createBlankModifyCriteriaLayout()
        self.criteriaToggles = [ QCheckBox('')                              for i in range( self.userCriteriaN ) ]
        self.criteriaLabels  = [ QLabel( self.criteriaData[i]['criteria'] ) for i in range( self.userCriteriaN ) ]
        self.criteriaRemover = [ QPushButton('Remove', self)                for i in range( self.userCriteriaN ) ]

        for i in range( self.userCriteriaN ):
            self.criteriaLabels[i].setAlignment( Qt.AlignCenter )
            self.modifyCriteriaLayout.addWidget( self.criteriaToggles[i], 1+i, 0, Qt.AlignCenter )
            self.modifyCriteriaLayout.addWidget( self.criteriaLabels[i],  1+i, 2 )
            self.modifyCriteriaLayout.addWidget( self.criteriaRemover[i], 1+i, 1 )
            self.modifyCriteriaLayout.addWidget( self.criteriaTargets[i], 1+i, 3 )
            self.criteriaRemover[ i ].setCursor( QCursor( Qt.PointingHandCursor ) )
            self.criteriaRemover[ i ].setAccessibleDescription( str( i ) )
            self.criteriaToggles[ i ].setChecked( True )
            self.criteriaToggles[ i ].setAccessibleDescription( str( i ) )
            self.criteriaToggles[ i ].setCursor( QCursor( Qt.PointingHandCursor ) )
        #self.modifyCriteriaLayout.addWidget(QSpacerItem) ?

        # send the criteria order number with the signal when toggle or 'Remove' button is pressed
        map( lambda criteriaToggle: criteriaToggle.toggled.connect( lambda pressed: self.disableUserCriteria( pressed, criteriaToggle ) ), self.criteriaToggles )
        map( lambda removeButton: removeButton.clicked.connect( lambda pressed: self.removeCriteriaComparisonItem( pressed, removeButton ) ), self.criteriaRemover )
        self.modifyCriteriaGroupBox.setLayout( self.modifyCriteriaLayout )


    def addMetricalToData( self ):
        pass


    def addMetricalComparisonItems( self ):
        pass


    def changeEqTypeLabel( self ):
        self.eqTypeInputLabel.setText( str( self.eqTypeComboBox.currentText() ) + ' ($)' )
        self.eqTypeInputLabel.setAlignment( Qt.AlignCenter )


    def changeInputLayout( self ):
        self.clearLayout( self.inputLayout )
        self.loadData()
        self.createBlankInputLayout()
        self.populateInputLayout()


    # adds columns based on number of input options from user input
    # all rows of 'Input for Options to Compare' box
    def changeOptionNumberLayout( self ):
        # number of options to display and compare
        # index for ComboBox starts at 0, so add whichever number comes first
        userN = 1 + self.nOptionsComboBox.currentIndex()
        if userN == self.userOptionN:  return
        else:   
            self.saveData()    
            self.userOptionN  = userN
            self.changeInputLayout()


    # default criteria from example.py
    def changePalette( self ):
        if ( self.useStylePaletteCheckBox.isChecked() ):
            QApplication.setPalette( QApplication.style().standardPalette() )
        else:
            QApplication.setPalette( self.originalPalette )


    # default criteria from example.py
    def changeStyle( self, styleName ):
        QApplication.setStyle( QStyleFactory.create( styleName ) )
        self.changePalette()


    def clearLayout( self, layout ):
        for i in reversed( range( layout.count() ) ):
            widgetToRemove = layout.takeAt(i).widget()
            layout.removeWidget( widgetToRemove )
            widgetToRemove.setParent( None )


    def createBlankInputLayout( self ):
        self.inputLayout.addWidget( self.blankTopLeftLabel, 0, 0, Qt.AlignTop )
        for i in range( self.userOptionN ):
            self.inputLayout.addWidget( self.optionLabels[ i ], 0, i + 1, Qt.AlignTop )
            self.inputLayout.setColumnStretch( i + 1, 1 )

        self.inputLayout.addWidget( self.eqTypeInputLabel, 1, 0, Qt.AlignTop )
        self.eqTypeInputLabel.setAlignment( Qt.AlignCenter )
        self.inputLayout.setColumnStretch( 0, 0 )
        for i in range( self.userOptionN ):
            self.inputLayout.addWidget( self.costInputEdits[ i ], 1, i + 1, Qt.AlignTop )

        for i in range( self.userCriteriaN ):
            for j in range( self.userOptionN ):
                self.inputLayout.addWidget( self.criteriaLabels[ i ], i + 2, 0, Qt.AlignTop )
                self.inputLayout.addWidget( self.criteriaInputEdits[ i ][ j ], i + 2, j + 1, Qt.AlignTop)
                self.inputLayout.setRowStretch( i + 2, 1 )

        self.inputLayout.setRowStretch( 0, 0 )
        self.inputLayout.setRowStretch( 1, 1 )
        self.inputLayout.setColumnStretch( 0, 0 )
        self.inputGroupBox.setLayout( self.inputLayout )


    def createBlankModifyCriteriaLayout( self ):
        self.modifyCriteriaLayout.addWidget( self.modifyCriteriaHeader0, 0, 0, Qt.AlignTop )
        self.modifyCriteriaLayout.addWidget( self.modifyCriteriaHeader1, 0, 1, Qt.AlignTop )
        self.modifyCriteriaLayout.addWidget( self.modifyCriteriaHeader2, 0, 2, Qt.AlignTop )
        self.modifyCriteriaLayout.addWidget( self.modifyCriteriaHeader3, 0, 3, Qt.AlignTop )
        self.modifyCriteriaLayout.setRowStretch( 0, 0 )
        self.modifyCriteriaLayout.setColumnStretch( 0, 0 )
        self.modifyCriteriaLayout.setColumnStretch( 1, 0 )
        self.modifyCriteriaLayout.setColumnStretch( 2, 1 )
        self.modifyCriteriaLayout.setColumnStretch( 3, 1 )
        self.modifyCriteriaGroupBox.setLayout( self.modifyCriteriaLayout )


    # for user to choose the 'Cost Comparison' method and the 'Number of Options'
    # 'Specify Decision Evaluation Display Characteristics' box
    def createFormatGroupBox( self ):
        self.formatGroupBox = QGroupBox( 'Specify Decision Evaluation Display Characteristics' )
        self.eqTypeComboBox = QComboBox()
        self.eqTypeComboBox.addItems( [ 'Nominal Cost', 'Present Equivalence', 'Future Equivalence', 'Annual Equivalence', 'Life-Cycle Cost' ] )
        self.eqTypeComboBox.setCurrentIndex( 0 )
        eqTypeLabel = QLabel( '&Cost Comparison:' )
        eqTypeLabel.setBuddy( self.eqTypeComboBox )

        self.nOptionsComboBox = QComboBox()
        self.nOptionsComboBox.addItems( self.nOptionsList )
        self.nOptionsComboBox.setCurrentIndex( 0 )
        nOptionsLabel = QLabel( '&Number of Options:' )
        nOptionsLabel.setBuddy( self.nOptionsComboBox )

        layout = QGridLayout()
        layout.addWidget( eqTypeLabel, 0, 0 )
        layout.addWidget( self.eqTypeComboBox, 0, 1 )
        layout.addWidget( nOptionsLabel, 1, 0 )
        layout.addWidget( self.nOptionsComboBox, 1, 1 )

        self.eqTypeComboBox.activated[ str ].connect( self.changeEqTypeLabel )
        self.nOptionsComboBox.activated[ int ].connect( self.changeOptionNumberLayout )
        self.formatGroupBox.setLayout( layout )


    # creates line edit for user to enter in their custom comparison items or 'Criterias'
    def createEnterCriteriaGroupBox( self ):
        self.enterCriteriaGroupBox = QGroupBox( 'Add Criteria and Funcational Metrics to Compare' )
        criteriaDescriptionLabel   = QLabel( '  Enter Criterion' )
        criteriaDescriptionLabel.setWordWrap( True )
        criteriaDescriptionLabel.setStyleSheet( 'QLabel { color : blue }' )
        metricalDescriptionLabel   = QLabel( '  Enter Functionality Metric' )
        metricalDescriptionLabel.setWordWrap( True )
        metricalDescriptionLabel.setStyleSheet( 'QLabel { color : green }' )

        # pressing return runs through the attached code twice, but the extra entry is removed from the criteria list
        self.userCriteriaEdit = QLineEdit('')
        self.userMetricalEdit = QLineEdit('')
        self.userAddCriteriaButton = QPushButton( 'Add' )
        self.userAddMetricalButton = QPushButton( 'Add' )
        self.userAddCriteriaButton.clicked.connect( self.addCriteriaToData )
        self.userAddMetricalButton.clicked.connect( self.addMetricalToData )
        self.userCriteriaEdit.returnPressed.connect( self.addCriteriaToData )
        self.userMetricalEdit.returnPressed.connect( self.addMetricalToData )
        self.userAddCriteriaButton.setCursor( QCursor( Qt.PointingHandCursor ) )
        self.userAddMetricalButton.setCursor( QCursor( Qt.PointingHandCursor ) )

        layout = QGridLayout()
        layout.addWidget( criteriaDescriptionLabel,   0, 0 )
        layout.addWidget( self.userCriteriaEdit,      0, 1 )
        layout.addWidget( self.userAddCriteriaButton, 0, 2 )
        layout.addWidget( metricalDescriptionLabel,   1, 0 )
        layout.addWidget( self.userMetricalEdit,      1, 1 )
        layout.addWidget( self.userAddMetricalButton, 1, 2 )
        layout.setColumnStretch( 0, 1 )
        layout.setColumnStretch( 1, 1 )
        layout.setColumnStretch( 2, 0 )
        self.enterCriteriaGroupBox.setLayout( layout )


    # creates the input matrix, which responds to the criteria items and number of options set by user
    # 'Input for Options to Compare' box
    def createInputGroupBox( self ):
        self.inputGroupBox     = QGroupBox( 'Input for Options to Compare' )
        self.inputLayout       = QGridLayout( self.inputGroupBox )
        self.blankTopLeftLabel = QLabel('')
        self.blankTopLeftLabel.setAccessibleDescription( 'blank' )
        self.blankTopLeftLabel.setAlignment( Qt.AlignCenter )
        self.eqTypeInputLabel  = QLabel( str( self.eqTypeComboBox.currentText() ) + ' ($)' )
        self.eqTypeInputLabel.setAccessibleDescription( 'eqTypeInputLabel' )
        self.eqTypeInputLabel.setAlignment( Qt.AlignCenter )
        self.createBlankInputLayout()


    # creates blank layout, which will take the user's criterias and organize them (alphabetically?)
    def createModifyCriteriaGroupBox( self ):
        self.modifyCriteriaGroupBox = QGroupBox( 'Criteria Details' )
        self.modifyCriteriaLayout   = QGridLayout()
        self.modifyCriteriaHeader0  = QLabel( 'Include in Plot?' )
        self.modifyCriteriaHeader2  = QLabel( 'Alphabetical Criteria Names' )
        self.modifyCriteriaHeader1  = QLabel( 'Remove From List' )
        self.modifyCriteriaHeader3  = QLabel( 'Target Value' ) 
        self.modifyCriteriaHeader0.setAlignment( Qt.AlignCenter )
        self.modifyCriteriaHeader2.setAlignment( Qt.AlignCenter )
        self.modifyCriteriaHeader1.setAlignment( Qt.AlignCenter )
        self.modifyCriteriaHeader3.setAlignment( Qt.AlignCenter )
        self.createBlankModifyCriteriaLayout()


    def createUpdatePlotGroupBox( self ):
        self.updatePlotGroupBox      = QGroupBox ( 'Click to Update Decision Evaluation Display' )
        self.updatePlotLayout        = QVBoxLayout()
        self.updatePlotFeedbackLabel = QLabel('this will be updated with success or failure')
        self.updatePlotPushButton    = QPushButton( 'Create/Update Decision Evaluation Display' )
        self.updatePlotPushButton.clicked.connect( self.updatePlot )
        self.updatePlotPushButton.setCursor( QCursor( Qt.PointingHandCursor ) )
        self.updatePlotFeedbackLabel.setAlignment( Qt.AlignCenter )
        self.updatePlotFeedbackLabel.setWordWrap( True )
        self.updatePlotLayout.addWidget( self.updatePlotPushButton    )
        self.updatePlotLayout.addWidget( self.updatePlotFeedbackLabel )
        self.updatePlotGroupBox.setLayout( self.updatePlotLayout )


    # responds to the toggle by each criteria in 'Comparison Items' box
    def disable_enable_UserCriteria( self, pressed, whichToggle ):
        index = int( whichToggle.accessibleDescription() )
        if pressed is True: 
            print 'adding criteria to plot'
            # do something with index
        elif pressed is False:
            print 'removing criteria from plot'
            # do something with index
        else: return


    def loadData(self):
        self.nOptionsList       = [   str( i + 1 )                       for i in range( self.maxOptions   ) ]
        self.optionLabels       = [   QLabel( 'Option ' + str( i + 1 ) ) for i in range( self.maxOptions   ) ]
        self.costInputEdits     = [   QDoubleSpinBox()                   for i in range( self.maxOptions   ) ] # what is the difference between QLineEdit('') and QLineEdit(self) ?
        self.criteriaLabels     = [   QLabel('')                         for i in range( self.maxCriterias ) ]
        self.criteriaTargets    = [   QDoubleSpinBox()                   for i in range( self.maxCriterias ) ]
        self.criteriaInputEdits = [ [ QDoubleSpinBox()                   for i in range( self.maxOptions   ) ]   for j in range( self.maxCriterias ) ] # matrix of QLineEdits (maxCriterias x maxOptions)

        for i in range( self.maxOptions ):
            self.costInputEdits[ i ].setAccessibleDescription( 'cost' + str( i + 1 ) )
            self.costInputEdits[ i ].setRange( 0, self.maxCost )
            self.optionLabels[ i ].setAccessibleDescription( 'Option' + str( i + 1 ) )
            for j in range( self.maxCriterias ):
                self.criteriaInputEdits[ j ][ i ].setRange( 0, 200.00 ) # percent effectiveness
                self.criteriaInputEdits[ j ][ i ].setAccessibleDescription(  'fun' + str( j + 1 ) + str( i + 1 ) )
                if i is 0:
                    self.criteriaTargets[j].setAccessibleDescription( 'targ' + str( j+1 ) )
                    self.criteriaLabels[j].setAccessibleDescription(  'fun'  + str( j+1 ) )


    def populateInputLayout( self ):
        items = [ self.inputLayout.itemAt( i ).widget() for i in range( self.inputLayout.count() ) ]
        for item in items:
            try:
                if str( item.accessibleDescription() ) == 'blank' or str( item.accessibleDescription() )[:6] == 'Option' or str( item.accessibleDescription() ) == 'eqTypeInputLabel':
                    continue
                elif type( item ) is QLabel:
                    criteriaNumber = int( str( item.accessibleDescription() )[ 3 ] )
                    self.criteriaLabels[ criteriaNumber - 1 ].setText( self.criteriaData[ criteriaNumber - 1 ][ 'criteria' ] )
                    self.criteriaLabels[ criteriaNumber - 1 ].setAlignment( Qt.AlignCenter )
                elif str( item.accessibleDescription() )[ :4 ] == 'cost':
                    optionNumber   = int( str( item.accessibleDescription() )[ 4 ] )
                    self.costInputEdits[ optionNumber - 1 ].setValue( self.costData[ 0 ][ optionNumber ] )
                elif str( item.accessibleDescription() )[ :3 ] == 'fun':
                    criteriaNumber = int( str( item.accessibleDescription() )[ 3 ] )
                    optionNumber   = int( str( item.accessibleDescription() )[ 4 ] )
                    self.criteriaInputEdits[ criteriaNumber - 1 ][ optionNumber - 1 ].setValue( self.criteriaData[ criteriaNumber - 1 ][ optionNumber ] )
                else:          continue
            except IndexError: continue


    # responds to the button by each criteria in 'Comparison Items' box
    def removeCriteriaComparisonItem( self, pressed, whichButton ):
        index = int( whichButton.accessibleDescription() )
        self.userCriteriaN -= 1
        self.criteriaData   = np.delete( self.criteriaData, index, 0 )
        self.addCriteriaComparisonItems()
        self.changeInputLayout()


    def runOnce( self ):
        self.emptyCellStr = 'empty'
        self.maxCost      = 5000000000.00
        self.maxOptions   = 5
        self.maxCriterias = 5
        self.dataNames    = [ 'criteria' ] + [ 'target' ] + [ 'op' + str( i ) for i in range( 1, 1+self.maxOptions ) ]
        dataTypes         = [ '|S33' ]     + [ 'float64'  for i in range( 1+self.maxOptions ) ]
        self.dtype        = { 'names': tuple( self.dataNames ), 'formats': tuple( dataTypes ) }
        self.costData     = np.zeros( 1,                  self.dtype )
        self.criteriaData = np.zeros( self.userCriteriaN, self.dtype )


    # creates a self.criteriaData np array to save user data
    # so if they change options or criterias, they need not re-enter data
    def saveData( self ):
        items = [ self.inputLayout.itemAt( i ).widget() for i in range( self.inputLayout.count() ) ]
        for item in items:
            if str( item.accessibleDescription() ) == 'blank' or str( item.accessibleDescription() )[:6] == 'Option':
                continue
            elif str( item.accessibleDescription() ) == 'eqTypeInputLabel': 
                self.costData[ 0 ][ 'criteria' ] = str( item.text() )
            elif type( item ) is QLabel:
                criteriaNumber = int( str( item.accessibleDescription() )[ 3 ] )
                self.criteriaData[ criteriaNumber-1 ][ 'criteria' ] = str( item.text() )
            elif str( item.accessibleDescription() )[ :4 ] == 'cost':
                optionNumber   = str( item.accessibleDescription() )[ 4 ]
                self.costData[0]['op'+optionNumber] = float( item.value() )
            elif str( item.accessibleDescription() )[ :3 ] == 'fun':                           
                criteriaNumber = int( str( item.accessibleDescription() )[ 3 ] )
                optionNumber   = str( item.accessibleDescription() )[ 4 ]
                self.criteriaData[ criteriaNumber-1 ][ 'op'+optionNumber ] = float( item.value() )
            else: continue

        if self.userCriteriaN > 0:
            items = [ self.modifyCriteriaLayout.itemAt( i ).widget() for i in range( self.modifyCriteriaLayout.count() ) ]
            for item in items:
                if type( item ) is QDoubleSpinBox:
                    criteriaNumber   = int( str( item.accessibleDescription() )[ 4 ] )
                    self.criteriaData[ criteriaNumber-1 ]['target'] = float( item.value() )


    def updatePlot( self ):
        self.saveData()
        multipleAxes_plotDED.createPlot( self )

    

if __name__ == '__main__':

    import os
    import sys
    import numpy as np
    import multipleAxes_plotDED

    # # for windows screen
    # from win32api import GetSystemMetrics
    # print("Width =", GetSystemMetrics(0))
    # print("Height =", GetSystemMetrics(1))

    # this may not work with windows/mac

    app     = QApplication( sys.argv )
    screen  = app.desktop().screenGeometry()
    w, h    = screen.width(), screen.height()
    gallery = DecisionEvaluationDisplay()
    gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    gallery.resize( 0.6*w, 0.6*h )
    gallery.show()
    sys.exit( app.exec_() )
