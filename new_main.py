# -*- coding: utf-8 -*-
"""
======== PTd Calculator ===========

Version: 0.8(alfa)
Created on Mon 30.09.2024 at 22:24:44
Last changes: Thi 22.11.2024
@author: Nikita Sozykin (nikita.sozykin@mail.ru)

This is the main file that contains UI and some data manipulation methods, like polyfitting,
roots and chemical potential calculations. 
"""


# General
from DataClass import Data


# Design
import sys 
import numpy as np
from PyQt5 import QtWidgets
from timer import Timer
import GUI

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class App(GUI.Ui_MainWindow, QtWidgets.QMainWindow, Data, Timer):
    
    # Plots arrays:
    figure = []
    static_canvas = []
    _static_ax = []
    
    # Artists:
    current_artist = None
    current_isotherm = None
    cur_artist_edgecolor = None
    
    
    # Main:
    Data = None
    borders = []
    fitting_isotherms_ended = False
    fitting_Mu_ended = False
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connects()
        self.plots_init()
        self.timer = Timer()
        
        
    def connects(self):
        self.actionIsotherm.triggered.connect(self.openNewIsotherm)
        self.actionIsodelta.triggered.connect(self.openNewIsodelta)
        self.extractButton.setEnabled(False)
        
        self.plots_layouts = [[self.horizontalLayout_2, self.horizontalLayout_4],           # Plot on Tab1
                              [self.horizontalLayout_10, self.horizontalLayout_7]]          # Plot on Tab2
    
    
    def openNewIsotherm(self):
        return self.openNewData("isotherm")
    
    def openNewIsodelta(self):
        return self.openNewData("isodelta")
    
    
    def openNewData(self, mode):
        self.Data = None
        self.Data = Data()
        
        try:
            self.Data.open_file(QtWidgets.QFileDialog.getOpenFileName(self, "Chose " + mode)[0], mode)
            self.Data.USED_T = self.Data.define_used_T(self.Data.table)
            self.Data.ISOTHERMS = self.Data.find_isotherms(self.Data.table, self.Data.USED_T)
            self.build_plots(0)
            self.build_plots(1)
    
        except Exception as e:
            print(e)

        
    def plots_init(self):
        for i in range(len(self.plots_layouts)):
            self.figure.append(Figure())
            self.static_canvas.append(FigureCanvas(self.figure[i]))
    
            self.plots_layouts[i][1].addWidget(NavigationToolbar(self.static_canvas[i], self))
            self.plots_layouts[i][0].addWidget(self.static_canvas[i])
            self._static_ax.append(self.static_canvas[i].figure.subplots())
            self.figure[i].tight_layout()
            
            self.static_canvas[i].mpl_connect('pick_event', self.onClick)
    
    
    def onClick(self, event):
        artist = event.artist
        
        if self.current_artist:
            self.current_artist.set_edgecolor(self.cur_artist_edgecolor)
            self.current_artist.set_sizes([30])
        self.current_artist = artist
        self.cur_artist_edgecolor = self.current_artist.get_edgecolor()
        
        artist.set(edgecolor = 'black')
        artist.set_sizes([100])
        self.static_canvas.draw()

        
    def build_plots(self, i):
        self._static_ax[i].clear()
        self._static_ax[i].grid(True)
        
        if i == 0:
            self._static_ax[i].set_xlabel(self.Data.table[0][0])
            self._static_ax[i].set_ylabel(self.Data.table[0][2])
            
            for k in range(len(self.Data.isotherms)):
                self._static_ax[i].scatter(self.Data.isotherms[k].body[1][0], 
                                           self.Data.isotherms[k].body[1][2],
                                               picker = 6, s=30)
                
                self._static_ax[i].text(max(self.Data.isotherms[k].body[1][0]), 
                                        max(self.Data.isotherms[k].body[1][2]),
                                                "T=" + str(round(self.Data.isotherms[k].body[0],-1)), size=6)
                
        if i == 1 and self.Data.chem_pots != []:
            
            self._static_ax[i].set_xlabel(self.Data.table.body[0][1])
            self._static_ax[i].set_ylabel("Chem Potential, kJ/mol")
            
            x = [np.mean(self.Data.isotherms[i].body[1][1]) for i in range(len(self.Data.chem_pots.body[0]))]
            
            for k in self.Data.chem_pots.body:
                self._static_ax[i].scatter(x, np.real(k)/1000, picker = True, s = 30)
    
        self.figure[i].tight_layout()
        self.static_canvas[i].draw()
    
    
    

def Open_main_window():
    module = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    module.exec_()
    
if __name__ == '__main__':
    Open_main_window()