#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_build import VM_CIBuildPlugin
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath


class VM_GradleBuildPlugin(VM_CIBuildPlugin):
    '''
    classdocs
    '''

    plugin_id=5
    
    def __init__(self,plugin_parameter_dict):
        VM_CIBuildPlugin.__init__(VM_GradleBuildPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_GradleBuildPlugin.plugin_id)
        self.gradle_command_line=self.get_parameter_value('gradle_command_line')
        self.gradle_target_path=self.get_parameter_value('gradle_target_path')
        self.build_tool_jdk=self.get_build_tool_jdk()
        self.build_tool_gradle=self.get_build_tool_gradle()
        self.gradle_file=self.get_parameter_value('gradle_file')
    
    def get_build_tool_jdk(self):
        result=0
        if self.get_parameter_value("build_tool_jdk"):
            result=self.get_parameter_value("build_tool_jdk")
        return result
    
    
        
    
    def get_build_tool_gradle(self):
        result=0
        if self.get_parameter_value("build_tool_gradle"):
            result=self.get_parameter_value("build_tool_gradle")
        return result
        
    def get_template_path(self):
        return CIPluginPath.gradle_build
    
    
   
    
    
    
                
        