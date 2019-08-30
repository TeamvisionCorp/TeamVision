#coding=utf-8
'''
Created on 2016-8-1

@author: Devuser
'''

import time

class VM_CIPlugin(object):
    '''
    classdocs
    '''


    def __init__(self,plugin_parameter_dict):
        self.plugin_parameter_dict=plugin_parameter_dict
        self.timstmap=str(time.time()).split('.')[1]
        self.plugin_using_name=VM_CIPlugin.get_parameter_value(self,"plugin_using_name")
    
    def get_enable_color(self):
        result="green"
        if self.is_enable()=="On":
            result="green"
        else:
            result="gray"
        return result
    
    def is_enable(self):
        result="On"
        if self.plugin_parameter_dict:
            if self.plugin_parameter_dict.get("is_enable"):
                result=self.plugin_parameter_dict.get("is_enable")
        return result
        
        
    def get_parameter_value(self,parameter_name,defalut=""):
        result=defalut
        if self.plugin_parameter_dict!=None:
            for parameter in self.plugin_parameter_dict['parameter']:
                if parameter.get('name')==parameter_name:
                    result=parameter.get('value')
        return result

    def get_controll_id(self):
        return int(time.time()*1000)