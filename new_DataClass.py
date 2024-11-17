# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:41:47 2024

@author: nikit
"""

import numpy as np
import statistics as stat

class Datafile():
    
    
    path = None
    version = None
    info = None
    table = None
    used_T = []
    isotherms = None
    mode = None
    
    
    def __init__(self):
        super().__init__() 
        
        
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
            self.table = [header, np.array(cutted_file)]
            
        if self.version == "v2":
            return "Not implemented yet. Coming soon!"
        
        
    def set_mode_byUser(self, mode):
        self.mode = mode
        
        
    def define_used_T(self, trashhold):
         
        sorted_T = self.table[1].sort(axis=self.table[0].index("T/C"))
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
        
        # Creating new array with isotherms:
            
        if self.used_T == []:
            self.define_used_T(3)
        else: None
        
        array = np.array(object, dtype=len(self.table[0].index("T/C")))
        for i in range(len(array)):
            array[i.append(self.used_T[i])]
        
        # if self.version == "v1":
        #     for k in self.used_T:
        #         for i in self.table[1][self.table[0].index("T/C")]:
        #             if abs(i-k)/k*100 < trashhold:
        #                 array.[self.used_T.index(k)].append(k, self.table[1][self.table[1].index()])
    
        for i,val1 in enumerate(self.used_T):
            array[i].append(val1)
            for k,val2 in enumerate(self.table[1]):
                if abs(val2[self.table[0].index("T/C")]-val1)/val1*100 < trashhold:
                    array[i].append(val2)
        self.isotherms = array
                        
        
        
        
                        
            
            
mode = 2
dataInst = Datafile()
if mode == 2:
    dataInst.set_path("C:\\Other stuff\\SciProgramms\\Python Programs\\dH_dS\\Example Data\\YSr2Cu175Fe125O7-isoterm.dat")
    dataInst.mode = "isotherm"
else: 
    dataInst.set_path("C:\\Other stuff\\SciProgramms\\Python Programs\\dH_dS\\Example Data\\YSr2Cu175Fe125O7_isocon.dat")
    dataInst.mode = "isodelta"
dataInst.define_version()
dataInst.pull_data()
dataInst.search_isotherms(3)


