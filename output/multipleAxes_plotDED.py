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

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy as np


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def createPlot(self):

    fontWeight = 'roman'
    size_title = 'xx-large'
    size_axes  = 'x-large'
    size_text  = 'large'

    if self.userCriteriaN is 0:
        self.updatePlotFeedbackLabel.setText('No Criteria to Compare! Add your own with the <Add Metrics, Criteria, or Qualities to Compare> window.')
        return


    print self.costData
    print self.criteriaData

    buff_axes  = 1.4
    buff_text  = 0.8 # in % of plot height
    plotColors = ['b', 'g', 'r', 'c', 'm']
    colorArray = [ plotColors[i] for i in range( self.userOptionN ) ] * self.userCriteriaN

    axesPositions = -0.2 * np.arange( self.userCriteriaN )[1:]

    x_values = np.array([ self.costData[0]['op'+str(i)]  for i in range( 1, 1+self.userOptionN )])
    y_values = np.array([ self.criteriaData['op'+str(i)] for i in range( 1, 1+self.userOptionN )])
    # y_values is now an NxM matrix where N=userCriteriaN and M=userOptionN
    # criterias are in reverse alphabetical order
    y_values = np.flip( np.transpose( y_values ), 0 )

    ded_fig, ded_ax = plt.subplots()
    ded_fig.subplots_adjust(left=0.3)
    ded_ax = [ ded_ax ]

    for i in range( 1, self.userCriteriaN ):
        ded_ax.append( ded_ax[0].twinx() )
        ded_ax[i].spines["left"].set_position(("axes", axesPositions[i-1] ))

    for i in range( 1, self.userCriteriaN ):
        make_patch_spines_invisible( ded_ax[i] )

    for i in range( 1, self.userCriteriaN ):
        ded_ax[i].spines["left"].set_visible( True )
        ded_ax[i].yaxis.set_label_position('left')
        ded_ax[i].yaxis.set_ticks_position('left')

    for i in range( self.userCriteriaN ):
        ded_ax[i].set_zorder( i+1 )

    criteriaMaximum = max(map(max, y_values ))
    for i in range( self.userOptionN ):
        ded_ax[0].axvline( x=x_values[i], ymin=0, ymax=buff_text, color='k' )
        ded_ax[0].text( x_values[i], buff_axes*0.83*criteriaMaximum, 'Option ' + str(i+1) + '\n$%.2f' % x_values[i], fontsize=size_text, fontweight=fontWeight )
    
    funs = []
    for i in range( self.userCriteriaN ):
        f_temp = ded_ax[i].scatter( x_values, y_values[i], c=plotColors[i], s=1000, alpha=0.8, label=self.criteriaData[self.userCriteriaN-1-i]['criteria'])
        funs.append( f_temp )
        ded_ax[i].set_ylabel( self.criteriaData[i]['criteria'], fontsize=size_axes, fontweight=fontWeight )
        ded_ax[i].set_xlim( 0, buff_axes * max( x_values ))
        ded_ax[i].set_ylim( 0, buff_axes * max( y_values[i] ))
        ded_ax[i].yaxis.label.set_color( plotColors[i] )
        ded_ax[i].tick_params(axis='y', colors=plotColors[i], labelsize=size_axes, length=19, width=2 )
        ded_ax[i].spines['right'].set_visible( False )
        ded_ax[i].spines['top'].set_visible( False )


    ded_ax[0].tick_params(axis='x', top=False, colors='k', labelsize=size_axes, length=12, width=1, direction='inout' )
    ded_ax[0].set_xlabel( str( self.eqTypeComboBox.currentText() ) + ' ($)', fontsize=size_axes, fontweight=fontWeight )
    ded_ax[0].set_title( 'Decision Evaluation Display', fontsize=size_title )
    ded_fig.patch.set_facecolor('w')
    plt.show()