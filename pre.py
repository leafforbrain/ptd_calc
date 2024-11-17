# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:43:43 2024

@author: nikit
"""

class Data():
    
    path = None
    version = None
    
    
    def __init__(self):
        super().__init__()
        
        
    def set_path(self, path):
        self.path = path
        
        
    def parse(self, data_path): # read & parse data from file

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


    def collect_data(self, data_path, data_type):
        
        parsed_file = self.parse(data_path)
        
        if data_type == "v1":
            
            # Collect Info:
            info = ' '.join([i for i in parsed_file[0].split() if "\"" not in i])
            header = parsed_file[0].split("\"")[:-1]
            header = [i.strip().rstrip() for i in header if i.strip().rstrip() != ""]
            
            # Extracting Table (nest-like form):
            cutted_file = [i.split() for i in parsed_file[1:]]
            #table_strings = cutted_file            <----   Can be used later
            
            table_rows = []
            cur_row = []
            
            for i in range(len(cutted_file[0])):
                for j in range(len(cutted_file)):
                    cur_row.append(cutted_file[j][i])
                table_rows.append(cur_row)
                cur_row = []
            
            table = [header, table_rows]
                
            return [info, table]
            
        if data_type == "v2":
            return "Not implemented yet. Coming soon!"
        
                

        
data = Preparations()
data.collect_data("C:\\Other stuff\\SciProgramms\\Python Programs\\dH_dS\Example Data\\x_Ca3Co4O9.dat","v1")
