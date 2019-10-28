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

# def plot( self, system_current ):
    # static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    # self.verticalLayout_resultsPlot.addWidget(static_canvas)
    # self.addToolBar(NavigationToolbar(static_canvas, self))

    # dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    # self.verticalLayout_resultsPlot.addWidget(dynamic_canvas)
    # self.addToolBar(QtCore.Qt.BottomToolBarArea,
    #                 NavigationToolbar(dynamic_canvas, self))

    # self._static_ax = static_canvas.figure.subplots()
    # t = np.linspace(0, 10, 501)
    # self._static_ax.plot(t, np.tan(t), ".")

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

    buff_axes  = 1.4
    buff_text  = 0.8 # in % of plot height
    vert_N     = len(y_values[0])
    axes_N     = len(y_values)
    axesPositions = -0.2 * np.arange( axes_N )[1:]

    self._static_ax = [ self._static_ax ]

    for i in range( 1, axes_N ):
        self._static_ax.append( self._static_ax[0].twinx() )
        self._static_ax[i].spines["left"].set_position(("axes", axesPositions[i-1] ))
        make_patch_spines_invisible( self._static_ax[i] )
        self._static_ax[i].spines["left"].set_visible( True )
        self._static_ax[i].yaxis.set_label_position('left')
        self._static_ax[i].yaxis.set_ticks_position('left')
        self._static_ax[i].set_zorder( i+1 )

    funs = []
    for i in range( axes_N ):
        f_temp = self._static_ax[i].scatter( x_values, y_values[i], s=1000, alpha=0.8)
        funs.append( f_temp )
        self._static_ax[i].spines['right'].set_visible( False )
        self._static_ax[i].spines['top'].set_visible( False )

    limits = self._static_ax[0].get_ylim()
    for val in x_values[0]:
        self._static_ax[0].axvline(x=val)

    self._static_ax[0].tick_params(axis='x', top=False, colors='k', labelsize=size_axes, length=12, width=1, direction='inout' )
    self._static_ax[0].set_title( 'Decision Evaluation Display', fontsize=size_title )

def plot( self, system_current ):
    clear_layout(self)
    self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    self.verticalLayout_resultsPlot.addWidget(self.static_canvas)
    self.toolbar = self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.static_canvas, self))
    self._static_ax = self.static_canvas.figure.subplots()

    x_variables = ['AELCC']
    y_variables = ['MTBF_average', 'P0', 'PFC']

    # which results to plot (selected from Tabular Results)
    iters_to_plot = TABLE.get_checked_iters(self)

    if iters_to_plot == []:
        print 'nothing to plot'
    else:
        x_values = system_current.simulated_values.loc[x_variables,iters_to_plot].values.tolist()
        y_values = system_current.simulated_values.loc[y_variables,iters_to_plot].values.tolist()
        create_plot( self, x_values, y_values  )

def clear_layout( self ):
    if getattr(self, 'toolbar', None):
        self.removeToolBar(self.toolbar)
    for i in reversed(range(self.verticalLayout_resultsPlot.count())): 
        self.verticalLayout_resultsPlot.itemAt(i).widget().setParent(None)