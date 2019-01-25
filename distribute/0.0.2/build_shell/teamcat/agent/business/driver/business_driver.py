#coding=utf-8
'''
Created on 2016-3-10

@author: Devuser
'''

import threading
from gatesidelib.common.simplelogger import SimpleLogger
class business_driver(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self,controller_message):
        threading.Thread.__init__(self)
        self.controller_message=controller_message
        self.thread_stop=False
        
    def stop(self):
        self.thread_stop=True
        SimpleLogger.info("stop thread")
    
    def is_matched(self,driver_key):
        '''
        根据driver name 判断是否适合处理当前请求
        返回值：True/False
        '''
        return False
        
        