#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from doraemon.home.models import TaskQueue

from doraemon.ci.viewmodels.vm_ci_task_queue import VM_CITaskQueue
from doraemon.project.models import Tag

class VM_CIAgent(object):
    '''
    classdocs
    '''


    def __init__(self,dm_agent,selected_agent_id):
        '''
        Constructor
        '''
        self.ci_agent=dm_agent
        self.selected_agent_id=selected_agent_id
    
    
    def is_selected(self):
        result=""
        if self.ci_agent.id==int(self.selected_agent_id):
            result="selected"
        return result
    
    def agent_tags(self):
        result=list()
        if self.ci_agent.AgentTags:
            for tag_id in eval(self.ci_agent.AgentTags):
                tmp_tag=Tag.objects.get(tag_id)
                if tmp_tag:
                    result.append(tmp_tag)              
        return result
    
    def agent_os(self):
        result="fa-windows"

        if self.ci_agent.OS==2:
            result="fa-linux"

        if self.ci_agent.OS==6:
            result="fa-apple"
        
        return result
    
    def agent_status_color(self):
        result="#32be77"

        if self.ci_agent.Status==3:
            result="gray"
        
        return result
    
    def agent_task_queues(self):
        result=list()
        task_queues_in_agent=TaskQueue.objects.get_agent_tasks(self.ci_agent.id)
        for tq in task_queues_in_agent:
            temp=VM_CITaskQueue(tq)
            result.append(temp)
        return result
   
    
    
    
                
        