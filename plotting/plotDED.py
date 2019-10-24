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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy as np

def createPlot(self):
    try:
        if self.userCriteriaN is 0:
            self.updatePlotFeedbackLabel.setText('No Criteria to Compare! Add your own with the <Add Metrics, Criteria, or Qualities to Compare> window.')
            return

        # should eventually import VT color pallette
        plotColors = ['b', 'g', 'r', 'c', 'm']
        colorArray = [ plotColors[i] for i in range( self.userOptionN ) ] * self.userCriteriaN

        fontWeight  = 'roman'
        size_title  = 'xx-large'
        size_axes   = 'x-large'
        size_text   = 'large'
        size_mark   = 200
        width_arow  = 5
        width_head  = 8
        width_tick  = 2
        width_x_ax  = 2
        width_y_ax  = 5
        width_line  = 3
        length_tick = 12

        buff_axes = 1.4  # ratio of visible x-axis compared to maximum x-value
        buff_perc = 10   # the percent plus/minus of box edges
        buff_gaps = 0.0    # space between vertical plot areas

        cost_target = self.costData['target']
        x_values = np.array([ self.costData[0]['op'+str(i)]  for i in range( 1, 1+self.userOptionN )])
        y_values = np.array([ self.criteriaData['op'+str(i)] for i in range( 1, 1+self.userOptionN )])
        y_values = np.transpose( y_values ) # to match data format, with options as columns

        counter = np.arange( 1, 1+self.userCriteriaN)
        y_lines = ( 2*counter-1 ) + ( counter*buff_gaps)
        targets = np.array( self.criteriaData['target'] )
        y_lines_array = np.repeat(y_lines, self.userCriteriaN).reshape((self.userCriteriaN,self.userOptionN))
        targets_array = np.repeat(targets, self.userCriteriaN).reshape((self.userCriteriaN,self.userOptionN))

        y_percs = np.true_divide(y_values,targets_array)-1
        y_plots = y_lines_array + ( np.true_divide( 100, buff_perc ) * y_percs )

        # for percentages [ 0, positive, negative]
        #strings = ['+bottom', '+bottom', '-top']
        y_bools = y_percs.astype('|S33')
        y_bools[y_percs>0]='+bottom'
        y_bools[y_percs<0]='-top'

        ded_fig, ded_ax = plt.subplots()
        patches = []

        for i in range( self.userCriteriaN ):
            new_patch = Rectangle((0,y_lines[i]-1), buff_axes*max(x_values), 2 )
            patches.append( new_patch )
            plt.axhline( y=y_lines[i], xmin=0,  xmax=buff_axes*max(x_values), 
                linewidth=width_line, 
                color=colorArray[i]
                )
            plt.scatter(x_values, y_plots[i], 
                marker='_', 
                s=size_mark, 
                c=colorArray[i], 
                edgecolors='face', 
                linewidths=width_line
                )
            for j in range( self.userOptionN ):
                #plt.annotate("{:.2f}%".format(y_percs[i,j]), xy=(x_values[j], y_plots[i,j]), xytext=(x_values[j], y_plots[i,j]-y_percs[i,j]), arrowprops=dict(arrowstyle='->'), horizontalalignment='right', verticalalignment='top' )
                plt.annotate('', xy=(x_values[j], y_plots[i,j]), xytext=(x_values[j], y_lines_array[i,j]), 
                    arrowprops=dict(width=width_arow, 
                        headwidth=width_head, 
                        edgecolor=colorArray[i], 
                        facecolor=colorArray[i]
                        ) 
                    )
        # same linewidth for vertical and horizontal appear different.. ?
        plt.axhline( linewidth=width_x_ax, color='k' )
        plt.axvline( linewidth=width_y_ax, color='k' )
        plt.xlim( 0,     buff_axes * max( x_values) )
        plt.ylim( 0, 1 + buff_gaps + max( y_lines ) )

        plt.xlabel( str( self.costData[0]['criteria'] ) + ' ($)', 
            fontsize=size_title, 
            fontweight=fontWeight 
            )
        plt.yticks( np.array(y_lines), np.array(self.criteriaData['criteria']), 
            rotation='horizontal', 
            fontsize=size_title, 
            fontweight=fontWeight 
            )
        plt.tick_params( axis='y', left=False, right=False )
        plt.tick_params( axis='x', top=False,   
            colors='k', 
            labelsize=size_axes, 
            length=length_tick, 
            width=width_tick, 
            direction='in' 
            )
        collection = PatchCollection(patches, 
            edgecolors='face', 
            facecolors=plotColors[:self.userCriteriaN], 
            alpha=0.1
            )
        ded_ax.add_collection(collection)
        xticks = ded_ax.xaxis.get_major_ticks()
        xticks[0].label1On = False
        xticks[0].label2On = True
        ded_ax.spines['right'].set_visible( False )
        ded_ax.spines['top'].set_visible( False )
        ded_fig.patch.set_facecolor('w')
        #plt.title( 'Decision Evaluation Display', fontsize=size_title )
        fig_man = plt.get_current_fig_manager()
        fig_man.resize(*fig_man.window.maxsize())
        plt.show()


    except Exception as e: 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)