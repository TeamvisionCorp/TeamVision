#coding=utf-8
'''
Created on 2016-8-23

@author: zhangtiande
'''

from teamvision.api.ci.viewmodel.vm_ci_task import VM_CITask
from teamvision.api.ci.viewmodel.vm_ci_agent import VM_CIAgent
from teamvision.api.ci.viewmodel.vm_ci_task_queue import VM_CITaskQueue


class CIFactory(object):
    '''
    classdocs
    '''
    
    
    @staticmethod
    def get_task(request):
        result=dict()
        if CIFactory.check_api_parameter(request):
            result=CIFactory.get_task_instance(request)
        return result
    
    
    
    @staticmethod
    def get_task_queue(request):
        queue_id=request.GET.get("tq_id")
        vm_task_queue=VM_CITaskQueue(queue_id)
        return vm_task_queue.__dict__
    
    
    @staticmethod
    def get_agent(request):
        agent_id=request.GET.get("agent_id")
        vm_ci_agent=VM_CIAgent(agent_id)
        return vm_ci_agent.__dict__
    
    
    @staticmethod
    def get_task_instance(request):
        task_id=request.GET.get("task_id")
        vm_ci_task=VM_CITask(task_id)
        return vm_ci_task.__dict__
    
    @staticmethod
    def check_api_parameter(request):
        result=True
        task_type=int(request.GET.get("task_type",0))
        if task_type!=0:
            if task_type not in (4,5,1):
                raise Exception("task_type is wrong!")
        return result
                
                
        
        
        