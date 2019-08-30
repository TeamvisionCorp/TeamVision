#coding=utf-8
'''
Created on 2015-11-4

@author: zhangtiande
'''
from django.shortcuts import HttpResponse
from teamvision.project.models import Project,Tag
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService

class VM_SystemRole(object):
    '''
    classdocs
    '''
    
    def __init__(self,system_role):
        self.role=system_role
        
    
    def user_name(self):
        result="Test"
#         if self.user.email:
#             result=result+" ("+self.user.email+")"
#         if not self.user.is_active:
#             result="<del>"+result+"</del>"
        return result
    
    def user_full_name(self):
        result="test"
#         if self.user.last_name and self.user.first_name:
#             result=self.user.last_name+self.user.first_name
        return result
    
    def user_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
#         if self.user.extend_info:
#             result=AccountService.get_avatar_url(self.user)
        return result