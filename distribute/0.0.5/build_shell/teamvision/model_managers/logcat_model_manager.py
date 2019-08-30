#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager


class LoggerManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(LoggerManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,logger_id):
        result=None
        try:
            result=super(LoggerManager,self).get_queryset().get(id=logger_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_by_deviceid(self,device_id):
        result=None
        try:
            result=self.all().filter(deviceId=device_id)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class BusinessLogManager(object):
    
    
    def __init__(self,model):
        self.model=model
    
    def all(self):
        return self.model.objects.all();
    
    def get(self,log_id):
        return self.model.objects.get(id=log_id);
    def get_by_deviceid(self,device_id):
        result=None
        try:
            result=self.model.objects.all().filter(deviceId=device_id)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
