#coding=utf-8
'''
Created on 2016-3-30

@author: zhangtiande
'''
    
import time
import threading

def timer_start():
    t=threading.Timer(0,test_func,("parameters",))
    t.start()
    
    
def test_func(msg1):
    print(time.time())
    time.sleep(5)
    print("I'm test_func,",msg1)
#     timer_start()

def timer2():
    timer_start()
    while True:
        time.sleep(1)
        timer_start()

if __name__=="__main__":
    timer2()
    
