#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_build import VM_CIBuildPlugin
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath


class VM_IOSBuildPlugin(VM_CIBuildPlugin):
    '''
    classdocs
    '''

    plugin_id=6
    
    def __init__(self,plugin_parameter_dict):
        VM_CIBuildPlugin.__init__(VM_IOSBuildPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_IOSBuildPlugin.plugin_id)
        self.build_tool_xcode=self.get_build_tool_xcode()
#         self.ios_command_line=self.get_parameter_value('ios_command_line')
        self.ios_target_path=self.get_parameter_value('ios_target_path')
        self.ios_build_provision=self.get_parameter_value('ios_build_provision')
        self.ios_build_crendentials=self.get_parameter_value('ios_build_crendentials')
        self.ios_build_target=self.get_parameter_value('ios_build_target')
        self.ios_build_parameter=self.get_parameter_value('ios_build_parameter')
        self.ios_project_dir=self.get_parameter_value('ios_project_dir')
        self.build_tool_pods=self.get_build_tool_pods()


        
    def get_template_path(self):
        return CIPluginPath.ios_build
    
    def get_build_tool_xcode(self):
        result=""
        if self.get_parameter_value("build_tool_xcode"):
            result=self.get_parameter_value("build_tool_xcode")
        return result
    
    def get_build_tool_pods(self):
        result=0
        if self.get_parameter_value("build_tool_pods"):
            result=self.get_parameter_value("build_tool_pods")
        return result
    
    
   
    
    
    
                
        