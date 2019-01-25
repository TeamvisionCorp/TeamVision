#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''


from business.ci.ci_task_config_service import CITaskConfigService
from doraemon.ci.viewmodels.vm_ci_task_basic_section import VM_BasicSection

class VM_CITaskConfig(object):
    '''
    classdocs
    '''


    def __init__(self,config_id):
        '''
        Constructor
        '''
        self.ci_task_config_dict=CITaskConfigService.get_ci_task_config(config_id)
    
    
    def get_basic_section(self):
        basic_section_dict=self.ci_task_config_dict['basic_section']
        return VM_BasicSection(basic_section_dict)
    
    def get_pre_section(self):
        result={}
        if self.ci_task_config_dict:
            result=self.ci_task_config_dict['pre_section']
        return result
    def get_scm_section(self):
        result={}
        if self.ci_task_config_dict:
            result=self.ci_task_config_dict['scm_section']
        return result
    
    def get_build_section(self):
        result={}
        if self.ci_task_config_dict:
            result=self.ci_task_config_dict['build_section']
        return result
    
    def get_post_section(self):
        result={}
        if self.ci_task_config_dict:
            result=self.ci_task_config_dict['post_section']
        return result
    
    
    
        
    
    
   
    
    
    
                
        