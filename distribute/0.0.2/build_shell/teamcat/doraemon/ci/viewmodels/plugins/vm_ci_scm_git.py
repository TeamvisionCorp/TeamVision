#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from doraemon.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from business.ci.ci_task_config_service import CITaskConfigService
from doraemon.ci.models import BasicSection,SCMSection,PreBuildSection,PostBuildSection,BuildSection
from doraemon.ci.models import CITaskPlugin
from doraemon.ci.pagefactory.ci_template_path import CIPluginPath


class VM_GitPlugin(VM_CIPlugin):
    '''
    classdocs
    '''

    plugin_id=2
    
    def __init__(self,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_GitPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_GitPlugin.plugin_id)
        self.repository_url=self.get_parameter_value('repository_url')
        self.local_directory=self.get_parameter_value('local_directory')
        self.ci_credentials=self.get_ci_credentials()
        self.git_check_out_strategy=self.get_check_out_strategy()
        self.branch=self.get_parameter_value('branch')
    
    def get_ci_credentials(self):
        result=0
        if self.get_parameter_value("ci_credentials"):
            result=int(self.get_parameter_value("ci_credentials"))
        return result
    
    def get_check_out_strategy(self):
        result=0
        if self.get_parameter_value("git_check_out_strategy"):
            result=int(self.get_parameter_value("git_check_out_strategy"))
        return result
        
    def get_template_path(self):
        return CIPluginPath.git_plugin
    
    
   
    
    
    
                
        