# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:43:43 2024

@author: nikit
"""
import statistics as stat, numpy as np
from table import Table



class DataFile(Table):
    
    path = None
    version = None
    info = None
    array = None
    table = None
    used_T = []
    fit_model = []
    fit_functions = []
    roots = []
    chem_pots = []
    isotherms = None
    mode = None
    
    
    def __init__(self):
        super().__init__(object)
        
        
    def set_path(self, path):
        self.path = path
        
        
    def parse(self, data_path):

        data = open(data_path)
        Iteration = iter(data)
        parsed_file = []
        
        while True:
            try:
                string = next(Iteration)
            except:
                StopIteration
                break
            parsed_file.append(string.rstrip())
        
        return parsed_file
    
    
    def define_version(self):
        
        if "Version" not in self.parse(self.path)[0].split(): self.version = "v1"
        else: None              #  <---- Version check here in future


    def pull_data(self):
        
        parsed_file = self.parse(self.path)
        
        if self.version == "v1":
            
            # Collect Info:
                
            self.info = ' '.join([i for i in parsed_file[0].split() if "\"" not in i])
            header = parsed_file[0].split("\"")[:-1]
            header = [i.strip().rstrip() for i in header if i.strip().rstrip() != ""]
            
            # Extracting Table (nest-like form):
                
            cutted_file = [i.split() for i in parsed_file[1:]]
            for i,val in enumerate(cutted_file):
                for j in range(len(val)):
                    cutted_file[i][j] = float(val[j])

            table_strings = cutted_file
            self.table = Table([header,table_strings])
            self.table.set_selected("strings")
            self.table.select_rows()
            
        if self.version == "v2":
            return "Not implemented yet. Coming soon!"
        
        
    def set_mode_byUser(self, mode):
        self.mode = mode
        
        
    def define_used_T(self, trashhold):
        
        self.used_T = []
        sorted_T = sorted(self.table.body[1][self.table.body[0].index("T/C")])
        curr_T = sorted_T[0:2]
        
        while True:
            try:
                for i,val in enumerate(sorted_T):
                    if abs(sorted_T[i]-stat.mean(curr_T))/stat.mean(curr_T)*100 < trashhold:
                        curr_T.append(sorted_T[i])
                sorted_T = [i for i in sorted_T if i not in curr_T]
                self.used_T.append(round(stat.mean(curr_T),-1))
                curr_T = sorted_T[0:2]
            except: break
        
        
    def search_isotherms(self, trashhold):
        
        self.define_used_T(3)
        self.isotherms = [[i,[]] for i in self.used_T]
        
        if self.version == "v1":
            
            for k in range(len(self.isotherms)):
                for i in self.table.select_strings()[1]:
                    if abs(i[self.table.body[0].index("T/C")]-self.isotherms[k][0])/self.isotherms[k][0]*100 < trashhold:
                        self.isotherms[k][1].append(i)
        
        # Revers selection in self.isotherms (strings ---> rows):
            
        for k in range(len(self.isotherms)):
            self.isotherms[k] = Table([self.isotherms[k][0],self.isotherms[k][1]])
            self.isotherms[k].set_selected("strings")
            self.isotherms[k].select_rows()
            
        
    
    def define_border_values(self):
        
        self.borders = []
        x_mins, y_mins, x_maxs, y_maxs = [], [], [], []
        
        
        for i in self.isotherms:
            x_mins.append(min(i.body[1][0]))
            y_mins.append(min(i.body[1][2]))
            x_maxs.append(max(i.body[1][0]))
            y_maxs.append(max(i.body[1][2]))
            
            x_min = min(x_mins)
            y_min = max(y_mins)
            x_max = max(x_maxs)
            y_max = min(y_maxs)

        self.borders = [x_min, y_min, x_max, y_max]

        
    def poly_fit_isotherms(self, order):  # Outputs fit model in the type: [[x's(T1),y's(T1)], [x's(T2),y's(T2)], ...]
        
        self.fit_model = []
        self.fit_functions = []
        isotherms_fit_xy = [None, None]
        
        if self.isotherms != None:
            for i in self.isotherms:
                isotherms_fit_xy[0] = np.arange(min(i.body[1][0]), max(i.body[1][0]), 0.05)
                isotherms_fit_xy[1] = np.polynomial.Polynomial.fit(i.body[1][0], i.body[1][2], order)(isotherms_fit_xy[0])
                self.fit_functions.append(np.polynomial.Polynomial.fit(i.body[1][0], i.body[1][2], order))
                self.fit_model.append(isotherms_fit_xy)
                isotherms_fit_xy = [None, None]
            
        else: 
            raise Exception
            print(Exception)
            
            
    def linear_fit_Mu(self, order):  # Outputs fit model in the type: [[x's(T1),y's(T1)], [x's(T2),y's(T2)], ...]
        
        self.linear_fit_model = []
        self.linear_fit_functions = []
        fit_xy = [None, None]
        
        if self.chem_pots != []:
            print(self.chem_pots.body)
            for i in self.chem_pots.body:
                
                fit_xy[0] = np.arange(min(i[1][0]), max(i[1][0]), 0.05)
                fit_xy[1] = np.polynomial.Polynomial.fit(i[1][0], i[1][2], order)(fit_xy[0])
                self.linear_fit_functions.append(np.polynomial.Polynomial.fit(i[1][0], i[1][2], order))
                self.linear_fit_model.append(fit_xy)
                fit_xy = [None, None]
            
        else: None
            # raise Exception
            # print(Exception)
            

# mode = 1
# dataInst = DataFile()
# if mode == 1:
#     dataInst.set_path("C:\\Other stuff\\SciProgramms\\Python Programs\\dH_dS\\Example Data\\YSr2Cu175Fe125O7-isoterm.dat")
#     dataInst.mode = "isotherm"
# else: dataInst.set_path("C:\\Other stuff\\SciProgramms\\Python Programs\\dH_dS\\Example Data\\YSr2Cu175Fe125O7-isocon.dat")
# dataInst.define_version()
# dataInst.pull_data()
# dataInst.search_isotherms(3)
# dataInst.poly_fit_isotherms(5)
# dataInst.poly_fit_Mu(5)
# # data.rearrange_data()