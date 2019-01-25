#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from business.testjob.testsubmitionservice import TestSubmitionService

class VM_TestJob(object):
    '''
    TestJOB business model
    '''
    
    def __init__(self,submition):
        ''' dm_testsubmition wapper
        '''
        self.testsubmition=submition
    
    def getproductname(self):
        return None
    
    def gettaskconfig(self):
        configname="--"
        return configname
    
    
    def getcaseset(self):
        caseset="--"
        if self.task.TaskCaseSet!=0:
            pass
            #caseset=DAL_CsaeSetQuery.getcaseset(self.TaskCaseSet).CaseSetQuery
        return caseset
    
    def getdependenttask(self):
        dependcyTask="--"
        if self.task.TaskDependentTask!=0:
            pass
            #caseset=DAL_CsaeSetQuery.getcaseset(self.task.TaskCaseSet).CaseSetQuery
        return dependcyTask
            
    def getbrowsers(self):
        browsers=[]
        if self.task.TaskBrowsers!=0:
            browsers=[1,2]
        return browsers
    
    def ismonitored(self):
        return self.task.TaskIsMonitored
    
    
    def getmachine(self):
        machine="--"
        if self.task.TaskMachine!=0:
            machine=""
        return machine
    
    def getstatus(self):
        return self.task.TaskStatus
    
    def getlastruntime(self):
        lastruntime="--"
        if self.task.TaskCreationTime!=None:
            lastruntime="03-05 12:23:45"
        return lastruntime
    
    def getrunenv(self):
        env="--"
        if self.task.TaskTestingConfigID!=0:
            env="Product"
        return env
            
    
    def haschild(self):
        ''' get this propertity by task id 
        '''
        return self.task.id