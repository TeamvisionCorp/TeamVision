#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''
from doraemon.ci.viewmodels.plugins.vm_ci_build import VM_CIBuildPlugin
from business.ci.ci_task_config_service import CITaskConfigService
from doraemon.ci.models import BasicSection,SCMSection,PreBuildSection,PostBuildSection,BuildSection
from doraemon.ci.models import CITaskPlugin
from doraemon.ci.pagefactory.ci_template_path import CIPluginPath

class VM_ShellCommandBuildPlugin(VM_CIBuildPlugin):
    '''
    classdocs
    '''
    plugin_id=4
    
    def __init__(self,plugin_parameter_dict):
        VM_CIBuildPlugin.__init__(VM_ShellCommandBuildPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_ShellCommandBuildPlugin.plugin_id)
        self.build_command_text=self.get_parameter_value('build_command_text')
        self.build_target_path=self.get_parameter_value('build_target_path')


    
    def get_template_path(self):
        return CIPluginPath.shell_build        
    
   
    
    
    
                
        