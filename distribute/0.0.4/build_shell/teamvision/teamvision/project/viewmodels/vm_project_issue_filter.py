#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from teamvision.project.models import ProjectRole, ProjectMember
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService

class VM_IssueFilter(object):
    '''
    classdocs
    '''


    def __init__(self,issue_filter,project_id):
        '''
        Constructor
        '''
        self.issue_filter=issue_filter
        self.project_id=project_id
    
    def project(self):
        result=0;
        if self.issue_filter:
            result=self.issue_filter.Project
        else:
            result=self.project_id
        return result
            
    
    def versions(self):
        return self.get_selected_field("Version");
    
    def processors(self):
        return self.get_selected_field("Processor");
    
    def creators(self):
        return self.get_selected_field("Creator");
    
    def severity(self):
        return self.get_selected_field("Severity");
    
    def solution(self):
        return self.get_selected_field("Solution");
    
    def status(self):
        return self.get_selected_field("Status");
    
    def create_date(self):
        result=self.get_selected_field("CreationTime")
        print(result)
        if result!=0 and len(result)!=0:
            result=result[0]+"-"+result[1]
        return result
    
    def get_selected_field(self,key):
        result=list()
        if self.issue_filter:
            if eval(self.issue_filter.FilterUIConfig).get(key):
                result=eval(self.issue_filter.FilterUIConfig).get(key)
        else:
            result=0
        return result
        
    
            
        
        