#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''

from doraemon.ci.models import CITask
from doraemon.api.ci.viewmodel.vm_ci_task_config import VM_CITaskConfig


class VM_CITask(object):
    '''
    classdocs
    '''


    def __init__(self,task_id):
        '''
        Constructor
        '''
        self.ci_task_id=int(task_id)
        self.project_id=self.get_ci_task().Project
        self.task_config=self.get_ci_task_config()
        self.deploy_service=self.get_ci_task().DeployService
        

    
    def get_ci_task(self):
        ci_task=CITask.objects.get(self.ci_task_id)
        if ci_task==None:
            raise Exception("ci task not exists with id "+str(self.ci_task_id))
        return ci_task
    
    def get_ci_task_config(self):
        result={}
        task_config=VM_CITaskConfig(self.get_ci_task().TaskConfig)
        result['basic_section']=task_config.get_basic_section()
        result['pre_section']=task_config.get_pre_section()
        result['scm_section']=task_config.get_scm_section()
        result['build_section']=task_config.get_build_section()
        result['post_section']=task_config.get_post_section()
        return result
        
    
    
    def get_task_agent(self):
        result=0
        if self.get_parameter_value(self.get_ci_task_config().get_basic_section(),"agent_filter_type")=='1':
            result=self.get_parameter_value(self.get_ci_task_config().get_basic_section(),"ci_agent_select")
        return result
    
    
    def get_agent_filters(self):
        result=""
        if self.get_parameter_value(self.get_ci_task_config().get_basic_section(),"agent_filter_type")=='2':
            result=self.get_parameter_value(self.get_ci_task_config().get_basic_section(),"agent_condations")
        return result
    
    def get_parameter_value(self,section,parameter_name):
        result=""
        if section['plugins']:
            for parameter in section['plugins'][0]['parameter']:
                if parameter.get('name')==parameter_name:
                    result=parameter.get('value')
        return result
        
        
    
    
   
    
    
    
                
        