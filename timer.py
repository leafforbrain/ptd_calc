# -*- coding: utf-8 -*-
import datetime
import time

class Timer():
    
    date = None
    state = None
    current_time = None
    start_time = None
    stop_time = None
    stop_duration = None
    continue_time = None
    finish_time = None
    ellapsed_time = None
    
    def __init__(self):
        super().__init__()
        self.date = datetime.datetime.now()
        
    def check(self):
        
        if self.state == "Started":
            self.current_time = time.perf_counter() - self.start_time
            return self.current_time
            
        elif self.state == "Continued":
            self.current_time = time.perf_counter() - self.start_time - self.stop_duration
            return self.current_time
        
    def start(self):
         
        if self.state in [None,"Finished"]:
            self.start_time = time.perf_counter()
            self.state = "Started"
        
        elif self.state == "Stoped":
            self.continue_time = time.perf_counter()
            self.stop_duration = self.continue_time - self.stop_time
            self.state = "Continued"
            
        elif self.state in ["Started","Continued"]:
            raise Exception("Timer is already started!")
            
    def stop(self):
        
        if self.state == "Started":
            self.stop_time = time.perf_counter()
            self.state = "Stoped"
           
        elif self.state in [None,"Stoped"]:
            raise Exception("Timer is not started!")
        
            
    def finish(self):
        
        if self.state in ["Started","Stoped"] and self.stop_duration == None:
            self.finish_time = time.perf_counter()
            self.ellapsed_time = round(self.finish_time - self.start_time, 3)
            self.state = "Finished"
        
        elif self.state == "Continued":
            self.finish_time = time.perf_counter()
            self.ellapsed_time = round(self.finish_time - self.start_time - self.stop_duration, 3)
            self.state = "Finished"
           
        elif self.state in [None,"Finished","Stoped"]:
            raise Exception("Timer is not started!")
            
# Test example:
# timerInst = Timer()
# timerInst.start()
# time.sleep(1)
# timerInst.stop()
# time.sleep(5)
# timerInst.start()
# time.sleep(1)
# timerInst.finish()
# print(timerInst.date)
# print(timerInst.stop_duration)
# print(timerInst.ellapsed_time)

