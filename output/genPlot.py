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
import pdb


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def createPlot( x_values, y_values ):

    fontWeight = 'roman'
    size_title = 'xx-large'
    size_axes  = 'x-large'
    size_text  = 'large'

    buff_axes  = 1.4
    buff_text  = 0.8 # in % of plot height
    vert_N     = len(y_values[0])
    axes_N     = len(y_values)
    axesPositions = -0.2 * np.arange( axes_N )[1:]

    ded_fig, ded_ax = plt.subplots()
    ded_fig.subplots_adjust(left=0.3)
    ded_ax = [ ded_ax ]

    for i in range( 1, axes_N ):
        ded_ax.append( ded_ax[0].twinx() )
        ded_ax[i].spines["left"].set_position(("axes", axesPositions[i-1] ))
        make_patch_spines_invisible( ded_ax[i] )
        ded_ax[i].spines["left"].set_visible( True )
        ded_ax[i].yaxis.set_label_position('left')
        ded_ax[i].yaxis.set_ticks_position('left')
        ded_ax[i].set_zorder( i+1 )

    funs = []
    for i in range( axes_N ):
        f_temp = ded_ax[i].scatter( x_values, y_values[i], s=1000, alpha=0.8)
        funs.append( f_temp )
        ded_ax[i].spines['right'].set_visible( False )
        ded_ax[i].spines['top'].set_visible( False )

    limits = ded_ax[0].get_ylim()
    pdb.set_trace()
    for val in x_values[0]:
        ded_ax[0].axvline(x=val)

    ded_ax[0].tick_params(axis='x', top=False, colors='k', labelsize=size_axes, length=12, width=1, direction='inout' )
    ded_ax[0].set_title( 'Decision Evaluation Display', fontsize=size_title )
    ded_fig.patch.set_facecolor('w')
    plt.show()