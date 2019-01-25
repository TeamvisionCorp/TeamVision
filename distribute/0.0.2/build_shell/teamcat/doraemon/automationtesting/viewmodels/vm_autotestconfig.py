#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.automationtesting.dal_autotestconfig import DAL_AutoTestConfig
from doraemon.automationtesting.datamodels.automationtaskenum import AutomationTaskStatusEnum

class VM_AutoTestConfig(object):
    '''
    AutomationTask business model
    '''
    
    def __init__(self,tesstconfig):
        ''' dm_automationtask wapper
        '''
        self.autotestconfig=tesstconfig
    
    def get_testconfig_name(self):
        return self.autotestconfig.TCFName
    
    def get_runtime(self):
        return '--'
#         config=None
#         if self.autotestconfig.TaskTestingConfig!=0:
#             config=DAL_TestingConfig.get_testingconfig(self.autotestconfig.TaskTestingConfig)
#         return config
    
    
    def get_testingenv(self):
        return '--'
#         caseset="--"
#         if self.autotestconfig.TaskCaseSet!=0:
#             pass
#             #caseset=DAL_CsaeSetQuery.getcaseset(self.TaskCaseSet).CaseSetQuery
#         return caseset
    

            
    def get_runtiming(self):
        runtime="--"
#         if self.autotestconfig.TaskRuntimeEnv!=0:
#             runtime=DAL_DictValue.get_dataname_by_datavalue("AutoTaskRuntime",self.autotestconfig.TaskRuntimeEnv)
#         else:
#             runtime=self.get_taskconfig().TCFName
        return runtime
    
    
    
    
    def get_status(self):
        return '--'
#         return DAL_DictValue.get_dataname_by_datavalue("AutoTaskStatus",self.autotestconfig.TaskStatus).DicDataName