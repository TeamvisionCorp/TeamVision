#coding=utf-8
'''
Created on 2015-10-23

@author: Devuser
'''
from doraemon.project.models import Task

class Task(object):
    '''
    classdocs
    '''


    def __init__(self,model_task):
        
        self.task=model_task
    
    def task_title(self):
        return Task.objects.get(id=self.task.TProjectID).TTitle