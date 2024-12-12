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
    table: TypeAlias = list[list[str], np.ndarray]
    
    SOURCE_PATH = None
    VERSION = None
    INFO = None
    MODE = None
    TABLE = None
    USED_T = None
    ISOTHERMS = None
    
    
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

    def create_table(self, file: pfile, version: float) -> np.ndarray:
        if version == 1:
            header = file[0].split("\"")[:-1]
            header = [i.strip().rstrip() for i in header if i.strip().rstrip() != ""]
            cutted_file = [i.split() for i in file[1:]]
            cutted_file = [[float(i[j]) for j in range(len(i))] for i in cutted_file]
            table =  np.array(cutted_file)
            
            return [header, table]
        
        else:   return "Not implemented yet. Coming soon!"
    
    def open_file(self, file: str, mode: str) -> None:
        self.set_spath(file)
        self.set_mode(mode)
        __parsed = Utils.parse(file)
        self.VERSION = self.define_ver(__parsed)
        self.INFO = self.collect_info(__parsed, self.VERSION)
        self.TABLE = self.create_table(__parsed, self.VERSION)

    def define_used_T(self, table: table, trashhold: float = 3) -> list[float]:
        sorted_Table = table[1][table[1][:, table[0].index('T/C')].argsort()]
        temperatures = sorted_Table[:,table[0].index('T/C')].tolist()

        curr_T = temperatures[0:2]
        used_T = []
        while True:         # <-- maybe lateeeer refactor
            try:
                for i in range(len(temperatures)):
                    if abs(temperatures[i]-stat.mean(curr_T))/stat.mean(curr_T)*100 < trashhold:
                        curr_T.append(temperatures[i])
                temperatures = [k for k in temperatures if k not in curr_T]
                used_T.append(round(stat.mean(curr_T),-1))
                curr_T = temperatures[0:2]
            except: break
        return used_T

    def find_isotherms(self, table: table, used_T: list[float], trashhold: float = 3, version: float = None) -> np.ndarray:
        isotherms = []    
        if version == 1.0:
            print(used_T)
            for k in used_T:
                columns = [i for i,val in enumerate(table[1][:, table[0].index("T/C")]) if abs(val-k)/k*100 < trashhold]
                isotherms.append(table[1][np.array(columns)])
        elif version == 'undefined':
            print('ERROR: Version undefined!')
        return isotherms
    
    def calc_Mu(self, isotherms: list[np.ndarray], contents_range: list, mode: str) -> np.ndarray:
           pass
    

                        
#data = Data()
#data.open_file('.\\Example Data\\YSr2Cu175Fe125O7-isocon.dat', mode='isodelta')
#data.open_file('.\\Example Data\\x_Ca3Co4O9.dat', mode='isotherm')
#data.USED_T = data.define_used_T(data.TABLE)
#data.find_isotherms(data.TABLE, data.USED_T, 1.0)
#print(data.USED_T)

