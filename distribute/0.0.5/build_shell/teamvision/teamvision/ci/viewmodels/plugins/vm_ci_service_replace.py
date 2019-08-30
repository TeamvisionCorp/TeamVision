#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from business.ci.ci_task_config_service import CITaskConfigService
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath
from bson import ObjectId

class VM_ServiceReplacePlugin(VM_CIPlugin):
    '''
    classdocs
    '''
    plugin_id=8
    
    def __init__(self,replace_config,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_ServiceReplacePlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_ServiceReplacePlugin.plugin_id)
        self.deploy_server=self.get_parameter_value('deploy_server',0)
        self.replace_file_ids=self.get_replace_file_ids('replace_file')
        self.replace_config=replace_config
    
    
    def get_replace_files(self):
        result=list()
        for file in self.get_service_files():
            temp=VM_CIServiceRPFile(file,self.replace_file_ids)
            result.append(temp)
        return result
    
    def get_replace_file_ids(self,parameter_name):
        result=list()
        if self.plugin_parameter_dict!=None:
            for parameter in self.plugin_parameter_dict['parameter']:
                if parameter.get('name')==parameter_name:
                    result.append(parameter.get('value'))
        return result

    
    def get_template_path(self):
        return CIPluginPath.service_replace_file
   
    
    
    
                
        