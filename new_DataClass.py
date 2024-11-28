# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:41:47 2024

@author: nikit
"""
from typing import TypeAlias
import numpy as np
import statistics as stat
from utils import Utils

class Data():
    
    pfile: TypeAlias = list[str]
    header: TypeAlias = list[str]
    table: TypeAlias = list[header, np.array]
    
    SOURCE_PATH = None
    VERSION = None
    INFO = None
    MODE = None
    TABLE = None
    USED_T = None
    isotherms = None
    
    
    def __init__(self):
        super().__init__() 
        
    def define_ver(self, file: pfile) -> float: #  <---- Version check here in future
        version = 1.0
        return version
    
    def set_ver(self, version: float) -> None:
        if version:
            self.VERSION = version
        else:
            try:
                self.VERSION = self.define_ver(self.SOURCE_PATH)
            except: 
                self.VERSION = 'undefined'
                raise ValueError

    def set_spath(self, path: str) -> None:
        self.SOURCE_PATH = path
    
    def set_mode(self, mode: str) -> None:
        self.MODE = mode
        
    def collect_info(self, file: pfile, version: float) -> str:
        if version == 1:
            info = ' '.join([i for i in file[0].split() if "\"" not in i])
            return info

    def collect_table(self, file: pfile, version: float) -> np.array:
        if version == 1:
            header = file[0].split("\"")[:-1]
            header = [i.strip().rstrip() for i in header if i.strip().rstrip() != ""]
            cutted_file = [i.split() for i in file[1:]]
            
            for i,val in enumerate(cutted_file):
                for j in range(len(val)):
                    cutted_file[i][j] = float(val[j])
                    
            table = [header, np.array(cutted_file)]
            return table
        
        else:   return "Not implemented yet. Coming soon!"
    
    def open_file(self, file: str, mode: str) -> None:
        self.set_spath(file)
        self.set_mode(mode)
        __parsed = Utils.parse(file)
        self.VERSION = self.define_ver(__parsed)
        self.INFO = self.collect_info(__parsed, self.VERSION)
        self.TABLE = self.collect_table(__parsed, self.VERSION)

    def define_used_T(self, table: table, trashhold: float = 3) -> list[float]:
        print(table[1])
        print("")
        sorted_T = table[1][table[1][:, table[0].index("T/C")].argsort()]
        print(table[1])
        curr_T = sorted_T[0:2]
        used_T = []
        
        while True:
            try:
                for i in range(len(sorted_T)):
                    if abs(sorted_T[i]-stat.mean(curr_T))/stat.mean(curr_T)*100 < trashhold:
                        curr_T.append(sorted_T[i])
                sorted_T = [k for k in sorted_T if k not in curr_T]
                used_T.append(round(stat.mean(curr_T),-1))
                curr_T = sorted_T[0:2]
            except: break
        return used_T

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
                        
data = Data()
data.open_file('.\\Example Data\\YSr2Cu175Fe125O7-isocon[750]edited.dat', mode='isotherm')
data.USED_T = data.define_used_T(data.TABLE)
print(data.USED_T)

