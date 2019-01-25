#coding=utf-8
#coding=utf-8
'''
Created on 2015-4-7

@author: 张天得
'''
from gatesidelib.common.simplelogger import SimpleLogger

def singleton(cls,*args,**kw):
    instances={}
    def _singleton():
        if cls not in instances:
            instances[cls]=cls(*args,**kw)
        return instances[cls]
    return _singleton




@singleton
class DriverPool(object):
    '''
    存数Step method中间数据
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.valuepool=dict()
    
    def put_value(self,key,value):
        if not self.valuepool.__contains__(key):
            self.valuepool[key]=value
    
    def has_value(self,key):
        return self.valuepool.__contains__(key)
        
    
    def get_value(self,key):
        result=None
        try:
            result=self.valuepool[key]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def clear(self,key):
        self.valuepool.pop(key)
    
    
    def clear_all(self):
        self.valuepool.clear()
    
    
        