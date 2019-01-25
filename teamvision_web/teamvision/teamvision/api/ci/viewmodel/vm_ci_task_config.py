#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''


from business.ci.ci_task_config_service import CITaskConfigService
from teamvision.ci.viewmodels.vm_ci_task_basic_section import VM_BasicSection

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
        return basic_section_dict
    
    def get_pre_section(self):
        pre_section_dict=self.ci_task_config_dict['pre_section']
        return pre_section_dict
    def get_scm_section(self):
        scm_section_dict=self.ci_task_config_dict['scm_section']
        return scm_section_dict
    
    def get_build_section(self):
        build_section_dict=self.ci_task_config_dict['build_section']
        return build_section_dict
    
    def get_post_section(self):
        post_section_dict=self.ci_task_config_dict['post_section']
        return post_section_dict
    
    
    
        
    
    
   
    
    
    
                
        