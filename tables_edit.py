# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:35:06 2024

@author: nikit
"""

class TableEdit():
    
    
    def __init__(self):
        super().__init__()
    
    
    def select_rows(self, str_values_table):
        
        table_rows = []
        cur_row = []
        
        for i in range(len(str_values_table[0])):
            for j in range(len(str_values_table)):
                cur_row.append(str_values_table[j][i])
            table_rows.append(cur_row)
            cur_row = []
        
        return table_rows
        

    def select_strings(self, row_values_table):
        
        table_strings = []
        cur_string = []
        
        for i in range(len(row_values_table[0])):
            for j in range(len(row_values_table)):
                cur_string.append(row_values_table[j][i])
            table_strings.append(cur_string)
            cur_string = []
        
        return table_strings
    
    
#    def sort_table_by_row(self, row):
        
        
        
        
    

# Test Example:
# table = TableSelectors()
# print(table.select_rows([
#                     [0,1,2,3],
#                     [4,5,6,7]
#                     ]))
# ---> [[0, 4], [1, 5], [2, 6], [3, 7]]

# print(table.select_strings([
#                     [0,4],
#                     [1,5],
#                     [2,6],
#                     [3,7]
#                     ]))
# ---> [[0, 1, 2, 3], [4, 5, 6, 7]]
        
        