#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from doraemon.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from doraemon.ci.models import CITaskPlugin
from doraemon.ci.pagefactory.ci_template_path import CIPluginPath


class VM_CIBuildPlugin(VM_CIPlugin):
    '''
    classdocs
    '''

    
    def __init__(self,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_CIBuildPlugin,plugin_parameter_dict)
        self.is_clean_outputs=VM_CIBuildPlugin.get_clean_outputs(self);
        self.is_upload_file=VM_CIBuildPlugin.get_is_upload_file(self)
    

    
    def get_clean_outputs(self):
        if not VM_CIBuildPlugin.get_parameter_value(self,'is_clean_outputs')=="":
            result=True
        else:
            result=False
        return result
    
    def get_is_upload_file(self):
        if not VM_CIBuildPlugin.get_parameter_value(self,'is_upload_file')=="":
            result=True
        else:
            result=False
        return result
    
    def is_clean_outputs_checked(self):
        if self.get_clean_outputs():
            return "checked"
        else:
            return ""
    def is_upload_file_checked(self):
        if self.get_is_upload_file():
            return "checked"
        else:
            return ""
        
    
   

    
    
   
    
    
    
                
        