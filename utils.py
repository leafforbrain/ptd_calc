"""Created on 28.11.2024 at 17:40"""




import numpy as np
from typing import TypeAlias



class Utils():

    pfile: TypeAlias = list[str]
    
    @staticmethod
    def parse(file: str) -> pfile:
        file = open(file)
        Iteration = iter(file)
        parsed_file = []
        while True:
            try:
                string = next(Iteration)
            except:
                StopIteration
                break
            parsed_file.append(string.rstrip())
        file.close()
        return parsed_file
    
    @staticmethod
    def print_with_header(header: list[str], nparray: np.ndarray) -> None:
        print(header)
        print(nparray)
        
   
    
    