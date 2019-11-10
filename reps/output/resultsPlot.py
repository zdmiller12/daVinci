import os
import numpy as np
from PyQt5 import QtCore

from easysettings import EasySettings

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

from . import resultsTable as TABLE
from . import markerMap as MAP

def make_patch_spines_invisible( ax ):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def plot_results(self, system_current):
    clear_layout(self)
    MM = MAP.create_marker_map()
    PP = self.preferences_plotting
    # easy enough to make drag and drop
    self.x_variables = ['TC']
    self.y_variables = ['MTBF_average', 'P0', 'PFC']
    yLabels = [PP.get('yLabelInner'), PP.get('yLabelMiddle'), PP.get('yLabelOuter')]

    # which results to plot (selected from Tabular Results)
    iters_to_plot = TABLE.get_checked_iters(self)

    if iters_to_plot == []:
        print('nothing to plot')
    else:
        x_values = system_current.simulated_values.loc[self.x_variables,iters_to_plot].values # .tolist()
        y_values = system_current.simulated_values.loc[self.y_variables,iters_to_plot].values # .tolist()

    vert_N = len(y_values[0])
    axes_N = len(y_values)
    axesPositions = -PP.get('yAxesSeparation')*np.arange(axes_N)[1:]

    color_template = ['b', 'g', 'r', 'c', 'm']

    self.fig, self.ax = plt.subplots()
    self.fig.subplots_adjust(left=PP.get('subplotAdjust'))
    self.ax = [self.ax]
    funs = []

    for i in range(1, axes_N):
        self.ax.append(self.ax[0].twinx())
        self.ax[i].spines["left"].set_position(("axes", axesPositions[i-1]))
        self.ax[i].spines["left"].set_color(color_template[i])
        # change color of spine too?  

    for i, ax in enumerate(self.ax):
        y_min = min(y_values[i])
        y_max = max(y_values[i])

        if len(x_values.shape) == 1:
            x_min = min(x_values)
            x_max = max(x_values)
        else:
            try:
                x_min = min(x_values[i])
                x_max = max(x_values[i])
            except:
                x_min = min(x_values[0])
                x_max = max(x_values[0])

        # add variable set to plot
        # with appropriate (buffered) limits
        ax.set_zorder(i+1)
        ax.set_xlim(x_min-(PP.get('bufferXAxis')*x_min), x_max+(PP.get('bufferXAxis')*x_max))
        ax.set_ylim(y_min-(PP.get('bufferYAxis')*y_min), y_max+(PP.get('bufferYAxis')*y_max))

        if PP.get('horizDataLineVisibility'):
            for j, val in enumerate(y_values[i]):
                xlim = ax.get_xlim()
                x_pos_perc = np.divide(x_values[0][j]-xlim[0], xlim[1]-xlim[0])
                ax.axhline(y=val, xmin=-1, xmax=x_pos_perc, c=color_template[i])

        # formatting (mostly axes)
        # make_patch_spines_invisible( ax )
        ax.spines["left"].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.label.set_color(color_template[i])
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', colors=color_template[i], labelsize=PP.get('axesLabelSize'), length=PP.get('tickLength'), width=PP.get('tickWidth'), direction=PP.get('tickPlacement'))
        ax.set_ylabel(yLabels[i], fontsize=PP.get('axesLabelSize'), fontweight=PP.get('fontStyle'))
        f_temp = ax.scatter(x_values, y_values[i], c=color_template[i], marker=MM[PP.get('markerShape')], s=PP.get('markerSize'), alpha=PP.get('markerTransparency'))
        funs.append(f_temp)

    if PP.get('vertDataLineVisibility'):
        for val in x_values[0]:
            self.ax[0].axvline(x=val, c=PP.get('vertDataLineColor'))

    self.ax[0].spines["bottom"].set_visible(True)
    self.ax[0].tick_params(axis='x', top=False, colors='k', labelsize=PP.get('axesLabelSize'), length=PP.get('tickLength'), width=PP.get('tickWidth'), direction=PP.get('tickPlacement'))
    self.ax[0].set_xlabel(PP.get('xLabel'), fontsize=PP.get('axesLabelSize'), fontweight=PP.get('fontStyle'))
    self.ax[0].set_title(PP.get('plotTitle'), fontsize=PP.get('sizeTitle'))
    self.fig.patch.set_facecolor('w')
    self.ax[0].grid(PP.get('gridVisibility'), which=PP.get('gridDensity'), axis=PP.get('gridDirection'), zorder=1)

    self.canvas = FigureCanvas(self.fig)
    self.verticalLayout_resultsPlot.addWidget(self.canvas)
    self.toolbar = NavigationToolbar(self.canvas, self)
    self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)

def clear_layout(self):
    try:
        self.removeToolBar(self.toolbar)
    except Exception as e:
        pass
    try:
        self.fig.clf()
    except Exception as e:
        pass
    for i in reversed(range(self.verticalLayout_resultsPlot.count())): 
        self.verticalLayout_resultsPlot.itemAt(i).widget().setParent(None)
