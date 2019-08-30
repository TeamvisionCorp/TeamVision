#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_build import VM_CIBuildPlugin
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath


class VM_IOSCommandBuildPlugin(VM_CIBuildPlugin):
    '''
    classdocs
    '''

    plugin_id=10
    
    def __init__(self,plugin_parameter_dict):
        VM_CIBuildPlugin.__init__(VM_IOSCommandBuildPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_IOSCommandBuildPlugin.plugin_id)
        self.build_tool_xcode=self.get_build_tool_xcode()
        self.ios_command_line=self.get_parameter_value('ios_command_line')
        self.ios_target_path=self.get_parameter_value('ios_target_path')


        
    def get_template_path(self):
        return CIPluginPath.ios_command_build
    
    def get_build_tool_xcode(self):
        result=""
        if self.get_parameter_value("build_tool_xcode"):
            result=self.get_parameter_value("build_tool_xcode")
        return result
    
    
   
    
    
    
                
        