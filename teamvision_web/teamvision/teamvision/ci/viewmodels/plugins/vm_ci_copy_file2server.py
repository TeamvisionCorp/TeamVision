#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from business.ci.ci_task_config_service import CITaskConfigService
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath
from teamvision.ci.viewmodels.vm_ci_service_replace_file import VM_CIServiceRPFile
from teamvision.ci.mongo_models import DeployServiceReplaceConfig
from bson import ObjectId

class VM_Copy2ServerPlugin(VM_CIPlugin):
    '''
    classdocs
    '''
    plugin_id=11
    
    def __init__(self,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_Copy2ServerPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_Copy2ServerPlugin.plugin_id)
        self.deploy_server=self.get_parameter_value('deploy_server',0)
        self.source_file=self.get_parameter_value('source_file')
        self.exec_command=self.get_parameter_value('exec_command')
        self.dest_dir=self.get_parameter_value('dest_dir')
        self.exclude_file=self.get_parameter_value('exclude_file')
    
    
    def get_template_path(self):
        return CIPluginPath.copy2_server
   
    
    
    
                
        