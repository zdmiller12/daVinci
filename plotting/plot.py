import sys
import time

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PyQt5 import QtCore

def plot( self ):
    static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    self.plot_results_system1.addWidget(static_canvas)
    self.addToolBar(NavigationToolbar(static_canvas, self))

    dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    self.plot_results_system1.addWidget(dynamic_canvas)
    self.addToolBar(QtCore.Qt.BottomToolBarArea,
                    NavigationToolbar(dynamic_canvas, self))

    self._static_ax = static_canvas.figure.subplots()
    t = np.linspace(0, 10, 501)
    self._static_ax.plot(t, np.tan(t), ".")