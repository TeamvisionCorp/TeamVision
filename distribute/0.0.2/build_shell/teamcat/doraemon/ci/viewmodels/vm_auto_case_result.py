#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''

from doraemon.ci.models import AutoTestingTaskResult,AutoCase,UnitTestCaseResult
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.home.models import Agent


class VM_AutoCaseResult(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_auto_case_result):
        self.auto_case_result=dm_auto_case_result
        
    
    @property
    def duration(self):
        result="--"
        if self.auto_case_result.StartTime and self.auto_case_result.EndTime:
            durations=(self.auto_case_result.EndTime-self.auto_case_result.StartTime).total_seconds()
            result=int(durations/60)
            if result==0:
                result=str(durations)+"秒"
            else:
                result=str(result)+"分钟"
        return result
    
   
    def case_name(self):
        result="--"
        try:
            test_case=AutoCase.objects.get(self.auto_case_result.TestCaseID)
            if test_case:#如果不为none，说明可以找到具体测试用例，找不到则认为是单元测试
                result=test_case.ClassName+test_case.CaseName
            else:
                result=self.auto_case_result.TestCaseName
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


    def device_name(self):
        result="--"
        task_result=AutoTestingTaskResult.objects.get(self.auto_case_result.TaskResultID)
        if task_result.MobileDeviceID:
            result="CellPhone"
        else:
            agent=Agent.objects.get(task_result.AgentID)
            if agent:
                result=agent.Name
        return result
     
    
    
    def is_success(self):
        result="status-default"
        if self.auto_case_result.Result==3:
            result="status-success"
        if self.auto_case_result.Result==2:
            result="status-fail"
        if self.auto_case_result.Result==1:
            result="status-cancel"
        return result
    