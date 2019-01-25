#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''

from doraemon.home.models import TaskQueue
from doraemon.ci.models import CITask


class VM_CITaskQueue(object):
    '''
    classdocs
    '''


    def __init__(self,queue_id):
        '''
        Constructor
        '''
        self.queue_id=queue_id
        self.task_id=self.get_task_queue().TaskID
        self.task_name=self.get_task_name()
        self.run_uuid=self.get_task_queue().TaskUUID
        self.task_type=self.get_task_queue().TaskType
    
    def get_task_queue(self):
        task_queue=TaskQueue.objects.get(int(self.queue_id))
        if task_queue==None:
            raise Exception("task queue not exists with id "+str(self.queue_id))
        return task_queue
    
    
    def get_task_name(self):
        ci_task=CITask.objects.get(int(self.task_id))
        if ci_task==None:
            raise Exception("task  not exists with id "+str(self.task_id))
        return ci_task.TaskName
    
    
    
    
   
    
    
    
                
        