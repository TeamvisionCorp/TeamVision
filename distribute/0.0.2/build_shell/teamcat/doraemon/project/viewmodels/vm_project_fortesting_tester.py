#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from doraemon.project.models import ProjectRole, ProjectMember
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from doraemon.project.viewmodels.vm_project_member import VM_ProjectMember

class VM_FortestingTester(object):
    '''
    classdocs
    '''


    def __init__(self,project_id,user,role_menu,login_user,fortesting):
        '''
        Constructor
        '''
        self.member=user
        self.project_id=project_id
        self.role_menu=role_menu
        self.fortesting=fortesting
    
    
    
    def is_fortesting_tester(self):
        result=""
        if self.fortesting!=None:
            if self.member.id in eval(self.fortesting.Testers):
                result="fa-check"
        return result
    
    
    
    def member_name(self):
        result=self.member.username
        if self.member.last_name and self.member.first_name:
            result=self.member.last_name+self.member.first_name
        return result
    
    def member_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        if self.member.extend_info:
            result=AccountService.get_avatar_url(self.member)
        return result
            
        
    
    