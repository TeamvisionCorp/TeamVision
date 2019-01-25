#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.automationtesting.dal_autotestconfig import DAL_AutoTestConfig
from doraemon.automationtesting.datamodels.automationtaskenum import AutomationTaskStatusEnum

class VM_AutomationTask(object):
    '''
    AutomationTask business model
    '''
    
    def __init__(self,automationtask):
        ''' dm_automationtask wapper
        '''
        self.autotask=automationtask
    
    def get_taskname(self):
        return self.autotask.TaskName
    
    def get_taskconfig(self):
        config=None
        if self.autotask.TaskTestingConfig!=0:
            config=DAL_AutoTestConfig.get_testingconfig(self.autotask.TaskTestingConfig)
        return config
    
    
    def get_caseset(self):
        caseset="--"
        if self.autotask.TaskCaseSet!=0:
            pass
            #caseset=DAL_CsaeSetQuery.getcaseset(self.TaskCaseSet).CaseSetQuery
        return caseset
    

            
    def get_runtime(self):
        runtime="--"
#         if self.autotask.TaskRuntimeEnv!=0:
#             runtime=DAL_DictValue.get_dataname_by_datavalue("AutoTaskRuntime",self.autotask.TaskRuntimeEnv)
#         else:
#             runtime=self.get_taskconfig().TCFName
        return runtime
    
    def is_persional(self):
        return self.autotask.TaskIsPersonal
    
    
    
    def get_status(self):
        return DAL_DictValue.get_dataname_by_datavalue("AutoTaskStatus",self.autotask.TaskStatus).DicDataName
    
    def get_lastruntime(self):
        lastruntime="--"
        if self.autotask.TaskLastRunTime!=None:
            lastruntime=self.autotask.TaskLastRunTime
        return lastruntime
    
    
    def get_sheduletime(self):
        sheduletime="--"
#         sheduletime=self.get_taskconfig().TCFRegularTiming
        return sheduletime
    
    def get_testingenv(self):
        env="--"
#         if self.autotask.TaskTestingConfigID!=0:
#             env="Product"
        return env
            
    
    def has_child(self):
        ''' get this propertity by autotask id 
        '''
        return self.autotask.id
    
    def is_running(self):
        result=True
        if self.autotask.TaskStatus==AutomationTaskStatusEnum.TaskStatus_New:
            result=False

        if self.autotask.TaskStatus==AutomationTaskStatusEnum.TaskStatus_Completed:
            result=False
        return result
        