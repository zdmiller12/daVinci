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


def saveFile ( self ):
    print 'you pressed save'

def newFile( self ):
    print 'you pressed new'

def openFile( self ):
    self.fileName = QFileDialog.getOpenFileName( self, 'Open CSV File', self.currentDirectory + os.path.sep + 'save', 'CSV Files (*.csv)')
    print 'got ' + str( self.fileName )

def quitFile( self ):
    # need to ask user to save first
    print 'goodbye for now...'
    sys.exit() 