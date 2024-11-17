# -*- coding: utf-8 -*-
"""
======== Table Class ===========
Version: 1.0 

This class contains methods on how to work with data tables in nest form (with rows_selected intially)

His methods works with table of type [[Header],[Table_Values]], and returns edited version of Table_Values
in the form, described higher. For now, Header remains unchanged by methods.

Created on Thu Oct  3 12:35:06 2024
Last changes: 11.10.24
@author: Nikita Sozykin (nikita.sozykin@mail.ru)

"""



class Table():
    
    body = None
    selected = None
    
    def __init__(self, body):
        # super().__init__()
        self.set_body(body)
        self.set_selected("rows")
    
    
    def set_body(self, body):
        self.body = body
        
        
    def set_selected(self, element):
        if element == "rows":
            self.selected = element
        elif element == "strings":
            self.selected = element
        else: 
            raise Exception("Bad selection")
            
            
    def select_rows(self):
        
        if self.selected == "rows":
            return self.body
        
        elif self.selected == "strings":
            table_rows = []
            cur_row = []

            for i in range(len(self.body[1][0])):
                for j in range(len(self.body[1])):
                    cur_row.append(self.body[1][j][i])
                table_rows.append(cur_row)
                cur_row = []

            self.selected = "rows"
            self.body[1] = table_rows
            
            return self.body
    
    def select_rows_in_table(self):
        
        if self.selected == "rows":
            return self.body
        
        elif self.selected == "strings":
            table_rows = []
            cur_row = []

            for i in range(len(self.body[0])):
                for j in range(len(self.body)):
                    cur_row.append(self.body[j][i])
                table_rows.append(cur_row)
                cur_row = []

            self.selected = "rows"
            self.body = table_rows
            
            return self.body
        
        
    def select_strings(self):
        
        if self.selected == "strings":
            return self.body
        
        elif self.selected == "rows":
            table_strings = []
            cur_string = []
            
            for i in range(len(self.body[1][0])):
                for j in range(len(self.body[1])):
                    cur_string.append(self.body[1][j][i])
                table_strings.append(cur_string)
                cur_string = []
        
            self.selected = "strings"
            self.body[1] = table_strings
            
            return self.body
        
        

# # Test Example:
# table = Table([["a","b","c","d"],  [[0,4],
#                                     [1,5],
#                                     [2,6],
#                                     [3,7]
#                                     ]])

# print(table.select_rows())
# # ---> [[0, 4], [1, 5], [2, 6], [3, 7]]
        
# print(table.select_strings())
# # ---> [[0, 1, 2, 3], [4, 5, 6, 7]]
