#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_build import VM_CIBuildPlugin
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath


class VM_AntBuildPlugin(VM_CIBuildPlugin):
    '''
    classdocs
    '''

    plugin_id=7
    
    def __init__(self,plugin_parameter_dict):
        VM_CIBuildPlugin.__init__(VM_AntBuildPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_AntBuildPlugin.plugin_id)
        self.ant_command_line=self.get_parameter_value('ant_command_line')
        self.ant_target_path=self.get_parameter_value('ant_target_path')
        self.build_tool_jdk=self.get_build_tool_jdk()
        self.ant_build_file=self.get_parameter_value('ant_build_file')
    
    def get_build_tool_jdk(self):
        result=0
        if self.get_parameter_value("build_tool_jdk"):
            result=self.get_parameter_value("build_tool_jdk")
        return result
        
    def get_template_path(self):
        return CIPluginPath.ant_build
    
    
   
    
    
    
                
        