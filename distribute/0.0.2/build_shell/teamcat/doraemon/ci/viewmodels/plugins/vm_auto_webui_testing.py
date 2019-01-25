#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from doraemon.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from doraemon.ci.models import CITaskPlugin
from doraemon.ci.pagefactory.ci_template_path import CIPluginPath


class VM_AutoWebUITestingPlugin(VM_CIPlugin):
    '''
    classdocs
    '''

    plugin_id=15
    
    def __init__(self,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_AutoWebUITestingPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_AutoWebUITestingPlugin.plugin_id)
        self.auto_log_dir=self.get_parameter_value('auto_log_dir')
        self.auto_project_dir=self.get_parameter_value('auto_project_dir')
        self.auto_tool_jdk=self.get_auto_tool_jdk()
        self.auto_host_info=self.get_auto_host_info()
        self.case_filters=self.get_case_filters()
    
    def get_auto_tool_jdk(self):
        result=0
        if self.get_parameter_value("auto_tool_jdk"):
            result=self.get_parameter_value("auto_tool_jdk")
        return result
    
    def get_auto_host_info(self):
        result=0
        if self.get_parameter_value("auto_host_info"):
            result=self.get_parameter_value("auto_host_info")
        return result
    
    def get_case_filters(self):
        result=""
        if self.get_parameter_value("autocase_filter"):
            result=self.get_parameter_value("autocase_filter")
        return result
        
    def get_template_path(self):
        return CIPluginPath.auto_webuitesting
    
    
    
   
    
    
    
                
        