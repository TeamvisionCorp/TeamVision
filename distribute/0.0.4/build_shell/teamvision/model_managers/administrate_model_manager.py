#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager


class DeviceManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        return super(DeviceManager,self).get_queryset().filter(IsActive=1)

    def android_device(self):
        return self.all().filter(DeviceOS=1)
    
    def ios_device(self):
        return self.all().filter(DeviceOS=2)
    
    def wp_device(self):
        return self.all().filter(DeviceOS=3)
    
    def lending_device(self):
        status_value=(2,3)
        return self.all().filter(DeviceStatus__in=status_value)
    
    def other(self):
        others=(4,5,6)
        return self.all().filter(DeviceType__in=others)
     
    def get(self,device_id):
        result=None
        try:
            result=super(DeviceManager,self).get_queryset().get(id=device_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class DeviceHistoryManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(DeviceHistoryManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,device_id):
        result=None
        try:
            result=super(DeviceHistoryManager,self).get_queryset().get(id=device_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
