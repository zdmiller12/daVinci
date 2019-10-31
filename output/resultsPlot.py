import numpy as np
from PyQt5 import QtCore

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

import resultsTable as TABLE


def make_patch_spines_invisible( ax ):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def create_plot( self, x_values, y_values ):
    fontWeight = 'roman'
    size_title = 'xx-large'
    size_axes  = 'x-large'
    size_text  = 'large'

    buffer_x_axis = 0.1
    buffer_y_axis = 0.1
    buffer_text   = 0.8 # in % of plot height

    vert_N     = len(y_values[0])
    axes_N     = len(y_values)
    axesPositions = -0.2 * np.arange( axes_N )[1:]

    color_template = ['b', 'g', 'r', 'c', 'm']

    self.fig, self.ax = plt.subplots()
    self.fig.subplots_adjust(left=0.33)
    self.ax = [ self.ax ]
    funs = []

    for i in range( 1, axes_N ):
        self.ax.append( self.ax[0].twinx() )
        self.ax[i].spines["left"].set_position(("axes", axesPositions[i-1] ))
        # change color of spine too?  

    for i, ax in enumerate(self.ax):
        y_min = min( y_values[i] )
        y_max = max( y_values[i] )

        if len(x_values.shape) == 1:
            x_min = min( x_values )
            x_max = max( x_values )
        else:
            try:
                x_min = min( x_values[i] )
                x_max = max( x_values[i] )
            except:
                x_min = min( x_values[0] )
                x_max = max( x_values[0] )


        # add variable set to plot
        f_temp = ax.scatter( x_values, y_values[i], c=color_template[i], s=1000, alpha=0.8)
        funs.append( f_temp )
        # with appropriate (buffered) limits
        ax.set_xlim( x_min-(buffer_x_axis*x_min), x_max+(buffer_x_axis*x_max) )
        ax.set_ylim( y_min-(buffer_y_axis*y_min), y_max+(buffer_y_axis*y_max) )

        # formatting (mostly axes)
        make_patch_spines_invisible( ax )
        ax.spines["left"].set_visible( True )
        ax.yaxis.label.set_color( color_template[i] )
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', colors=color_template[i], labelsize=size_axes, length=19, width=2 )
        ax.spines['right'].set_visible( False )
        ax.spines['top'].set_visible( False )
        ax.set_zorder( i+1 )

        ax.set_ylabel(self.y_variables[i], fontsize=size_axes, fontweight=fontWeight)

    for val in x_values[0]:
        self.ax[0].axvline(x=val, c='k')

    self.ax[0].tick_params(axis='x', top=False, colors='k', labelsize=size_axes, length=12, width=1, direction='inout' )
    self.ax[0].set_xlabel( str( self.x_variables[0] ) + ' ($)', fontsize=size_axes, fontweight=fontWeight )
    self.ax[0].set_title( 'Decision Evaluation Display', fontsize=size_title )
    self.fig.patch.set_facecolor('w')

    self.canvas = FigureCanvas(self.fig)
    self.verticalLayout_resultsPlot.addWidget(self.canvas)
    self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.canvas, self))

def plot( self, system_current ):
    clear_layout(self)

    # easy enough to make drag and drop
    self.x_variables = ['AELCC']
    self.y_variables = ['MTBF_average', 'P0', 'PFC']

    # which results to plot (selected from Tabular Results)
    iters_to_plot = TABLE.get_checked_iters(self)

    if iters_to_plot == []:
        print 'nothing to plot'
    else:
        x_values = system_current.simulated_values.loc[self.x_variables,iters_to_plot].values # .tolist()
        y_values = system_current.simulated_values.loc[self.y_variables,iters_to_plot].values # .tolist()
        create_plot( self, x_values, y_values  )

def clear_layout( self ):
    # # try:
    # #     self.removeToolBar()
    # # except Exception as e:
    # #     print e

    # if hasattr(self.static_canvas, 'toolbar'):
    #     self.removeToolBar(self.toolbar)
    # else:
    #     print 'no toolbar'
    for i in reversed(range(self.verticalLayout_resultsPlot.count())): 
        self.verticalLayout_resultsPlot.itemAt(i).widget().setParent(None)