#coding=utf-8
#coding=utf-8
'''
Created on 2017年4月26日

@author: ethan
'''

class VM_TaskParameterGroup(object):
    '''
    classdocs
    '''


    def __init__(self,dm_task_parameter_group):
        '''
        Constructor
        '''
        self.parameter_group=dm_task_parameter_group
    
    
    @property
    def group_type_name(self):
        result="Testing"
        group_type=self.parameter_group.group_type
        if group_type:
            if group_type==1:
                result="Release"
            if group_type==2:
                result="Testing"
            if group_type==3:
                result="Staging"
            if group_type==4:
                result="自定义"
        return result
                
            
            
        