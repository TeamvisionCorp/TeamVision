#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from doraemon.project.models import Tag
from gatesidelib.common.simplelogger import SimpleLogger

class VM_DataValue(object):
    '''
    classdocs
    '''


    def __init__(self,dm_data_value,selected_value,selected_text=""):
        '''
        Constructor
        '''
        self.dm_data_value=dm_data_value
        self.selected_value=selected_value
        self.selected_text=selected_text
    
    
    def is_selected(self):
        result=""
        try:
            if self.dm_data_value.DicDataValue==int(self.selected_value):
                result="selected"
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def is_text_selected(self):
        result=""
        if self.dm_data_value.DicDataName==self.selected_text:
            result="selected"
        return result
        
                 
            
        
   
    
    
    
                
        