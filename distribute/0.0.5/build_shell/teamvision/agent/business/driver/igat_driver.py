#coding=utf-8
'''
Created on 2016-3-11

@author: Devuser
'''
from agent.business.driver.business_driver import business_driver
from gatesidelib.common.simplelogger import SimpleLogger
import time

class igat_driver(business_driver):
    '''
    classdocs
    '''


    def __init__(self,controller_message):
        '''
        Constructor
        '''
        business_driver.__init__(self,controller_message)
    
    def run(self):
        while True:
            time.sleep(5)
            if not self.thread_stop:
                SimpleLogger.info("igat_driver")
            else:
                break
            
    def is_matched(self,driver_key):
        '''
        根据driver name 判断是否适合处理当前请求
        返回值：True/False
        '''
        if driver_key=="DRIVER_KEY":
            return True
        else:
            return False
    
    
    
        