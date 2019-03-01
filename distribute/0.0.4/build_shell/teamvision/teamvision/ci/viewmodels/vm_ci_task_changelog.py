#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''

from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.ci.viewmodels.vm_ci_history_changefile import VM_CIHistoryChangeFile
from business.ci.ci_task_history_service import CITaskHistoryService

class VM_CITaskChangeLog(object):
    '''
    classdocs
    '''
    
    def __init__(self,change_logs,index,repo):
        self.repo=repo
        self.change_logs=change_logs
        self.version=self.get_property('version')
        self.commit_time=self.get_property('timestamp')
        self.commitor=self.get_property('author')
        self.change_files=self.get_property('changes')
        self.index=index
        
    
    def change_file_list(self):
        result=list()
        try:
            if self.change_files:
                for file in self.change_files:
                    temp=VM_CIHistoryChangeFile(file)
                    result.append(temp)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    def get_message(self):
        commit_message=self.get_property('message')
        if not commit_message:
            commit_message="没有变更记录"
        return commit_message
           
    
    def get_property(self,key):
        result=""
        try:
            result=self.change_logs[key]
        except Exception as ex:
            SimpleLogger.exception(ex)
            
        return result