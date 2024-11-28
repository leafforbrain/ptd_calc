"""Created on 28.11.2024 at 17:40"""




class Utils():

    @staticmethod
    def parse(file: str):
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
    
   
    
    