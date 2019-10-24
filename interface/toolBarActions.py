#!/usr/bin/env python


#############################################################################
##
## Decision Evaluation Display
##
## Zachary Miller
## January 2019
## zdmiller12@gmail.com
##
#############################################################################

import os, sys
import numpy as np
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import plotDED

def saveFile ( self ):
    print 'save'


def newFile( self ):
    print 'new'


def openFile( self ):
    self.fileName = QFileDialog.getOpenFileName( self, 'Open CSV File', self.currentDirectory + os.path.sep + 'save', 'CSV Files (*.csv)')
    convertData( self )

def convertData( self ):
    pd_data = pd.read_csv( str( self.fileName[0] ) )
    self.np_head = pd_data.columns.values.tolist()
    self.np_data = pd_data.values.tolist()

    self.userCriteriaN = 0
    self.userMetricN   = 0
    self.userOptionN = len(self.np_head) - 2
    diff = self.maxOptions - self.userOptionN

    self.costData = np.zeros( self.userCriteriaN, self.dtype )
    self.criteriaData = np.zeros( self.userCriteriaN, self.dtype )
    self.metricData   = np.zeros( self.userMetricN,   self.dtype )

    for item in self.np_data:
        newTuple = tuple( item + [ float(0) ] * diff )
        if str(item[0])[:9]    != 'Criterion' and str(item[0])[:6] != 'Metric':
            self.costData       = np.append(self.costData,     np.array( [ newTuple ], self.dtype ) )
        elif str(item[0])[:9]  == 'Criterion':
            self.criteriaData   = np.append(self.criteriaData, np.array( [ newTuple ], self.dtype ) )
            self.userCriteriaN += 1
        elif str(item[0])[:6]  == 'Metric':
            self.metricData     = np.append(self.metricData,   np.array( [ newTuple ], self.dtype ) )
            self.userMetricN   += 1

    plotDED.createPlot( self )