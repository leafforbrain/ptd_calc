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
from data import DataFile, Table


# Design
import sys, numpy as np
from PyQt5 import QtWidgets
from timer import Timer
import GUI

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class App(GUI.Ui_MainWindow, QtWidgets.QMainWindow, DataFile, Table, Timer):
    
    # Plots arrays:
    figure = []
    static_canvas = []
    _static_ax = []
    
    # Artists:
    current_artist = None
    current_isotherm = None
    cur_artist_edgecolor = None
    
    
    # Main:
    new_DataFile = None
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
        self.comboBox.currentTextChanged.connect(self.points_steps_switch)
        self.polyfitButton.clicked.connect(self.poly_fitting_isotherms)
        self.linearFit_button.clicked.connect(self.linear_fitting_Mu)
        self.extractButton.clicked.connect(self.extract_mu)
        self.extractButton.setEnabled(False)
        
        self.plots_layouts = [[self.horizontalLayout_2, self.horizontalLayout_4],           # Plot on Tab1
                              [self.horizontalLayout_10, self.horizontalLayout_7]]          # Plot on Tab2
    
    
    def openNewIsotherm(self):
        return self.openNewData("isotherm")
    
    
    def openNewIsodelta(self):
        return self.openNewData("isodelta")
    
    
    def openNewData(self, mode):
        self.new_DataFile = None
        self.new_DataFile = DataFile()
        self.new_DataFile.set_path(QtWidgets.QFileDialog.getOpenFileName(self, "Chose " + mode)[0])
        
        try:
            self.new_DataFile.define_version()
            if self.new_DataFile.version == "v1" and mode != "":
                self.new_DataFile.set_mode_byUser(mode)
                
            elif self.new_DataFile.version != "v1":
                None            # <--- V2 level: automatic mode setting by pulling info from file
                
            self.new_DataFile.pull_data()
            self.new_DataFile.define_used_T(3)
            self.new_DataFile.search_isotherms(3)
            self.new_DataFile.define_border_values()
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
            self._static_ax[i].set_xlabel(self.new_DataFile.table.body[0][0])
            self._static_ax[i].set_ylabel(self.new_DataFile.table.body[0][2])
            
            for k in range(len(self.new_DataFile.isotherms)):
                self._static_ax[i].scatter(self.new_DataFile.isotherms[k].body[1][0], 
                                           self.new_DataFile.isotherms[k].body[1][2],
                                               picker = 6, s=30)
                
                self._static_ax[i].text(max(self.new_DataFile.isotherms[k].body[1][0]), 
                                        max(self.new_DataFile.isotherms[k].body[1][2]),
                                                "T=" + str(round(self.new_DataFile.isotherms[k].body[0],-1)), size=6)
                
        if i == 1 and self.new_DataFile.chem_pots != []:
            
            self._static_ax[i].set_xlabel(self.new_DataFile.table.body[0][1])
            self._static_ax[i].set_ylabel("Chem Potential, kJ/mol")
            
            x = [np.mean(self.new_DataFile.isotherms[i].body[1][1]) for i in range(len(self.new_DataFile.chem_pots.body[0]))]
            
            for k in self.new_DataFile.chem_pots.body:
                self._static_ax[i].scatter(x, np.real(k)/1000, picker = True, s = 30)
    
        self.figure[i].tight_layout()
        self.static_canvas[i].draw()
    
    
    def points_steps_switch(self):
        if self.comboBox.currentText() == "points":
            self.doubleSpinBox.setDecimals(0)
            self.doubleSpinBox.setMinimum(1)
            self.doubleSpinBox.setSingleStep(1)
        
        elif self.comboBox.currentText() == "step":
            self.doubleSpinBox.setDecimals(2)
            self.doubleSpinBox.setMinimum(0)
            self.doubleSpinBox.setSingleStep(0.01)
            
        
    def poly_fitting_isotherms(self):
        self.build_plots(0)
        self.new_DataFile.poly_fit_isotherms(self.spinBox.value())
        
        for i in self.new_DataFile.fit_model:
            self._static_ax[0].plot(i[0], i[1])

        self.figure[0].tight_layout()
        self.static_canvas[0].draw()
        self.fitting_isotherms_ended = True
        self.extractButton.setEnabled(True)
        
        
    def linear_fitting_Mu(self):
        self.build_plots(1)
        self.new_DataFile.poly_fit_Mu(1)
        
        for i in self.new_DataFile.linear_fit_model:
            self._static_ax[1].scatter(i[0], i[1], picker = True, s=30)

        self.figure[1].tight_layout()
        self.static_canvas[1].draw()
        self.fitting_Mu_ended = True
        
        
    def calculate_roots(self):
        self.new_DataFile.roots = []
        
        if self.comboBox.currentText() == "points":
            _range = np.linspace(self.new_DataFile.borders[1], self.new_DataFile.borders[3], int(self.doubleSpinBox.value()))
            
            for i in range(len(self.new_DataFile.fit_functions)):
                self.new_DataFile.roots.append([(self.new_DataFile.fit_functions[i]-k).roots().tolist() for k in _range])
           
        elif self.comboBox.currentText() == "step":
            _range = np.arange(self.new_DataFile.borders[1], self.new_DataFile.borders[3], self.doubleSpinBox.value())
            
            for i in range(len(self.new_DataFile.fit_functions)):
                self.new_DataFile.roots.append([(self.new_DataFile.fit_functions[i]-k).roots().tolist() for k in _range])
            
        for i in range(len(self.new_DataFile.roots)):
            self.new_DataFile.roots[i] = [np.real(k[0]) for k in self.new_DataFile.roots[i]]
                
            
    def calculate_mu(self):
        self.calculate_roots()
        print(self.new_DataFile.roots)
        self.new_DataFile.chem_pots = []
        
        m = self.new_DataFile.isotherms
        
        for i,val in enumerate(self.new_DataFile.roots):
                self.new_DataFile.chem_pots.append([8.314462/2*sum(m[i].body[1][1])/len(m[i].body[1][1])*val[k] for k in range(len(val))])
       
        self.new_DataFile.chem_pots = Table(self.new_DataFile.chem_pots)
        self.new_DataFile.chem_pots.set_selected("strings")
        # print("chems: ", self.new_DataFile.chem_pots.body)
        self.new_DataFile.chem_pots.select_rows_in_table()
        
        
    def extract_mu(self):
        self.calculate_mu()
        self.build_plots(1)
        
    

def Open_main_window():
    module = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    module.exec_()
    
if __name__ == '__main__':
    Open_main_window()