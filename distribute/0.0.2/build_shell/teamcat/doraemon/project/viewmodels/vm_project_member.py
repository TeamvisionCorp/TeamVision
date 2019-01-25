#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from doraemon.project.models import ProjectRole, ProjectMember
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from gatesidelib.common.simplelogger import SimpleLogger

class VM_ProjectMember(object):
    '''
    classdocs
    '''


    def __init__(self,project_id,user,role_menu,login_user,selected_member=0):
        '''
        Constructor
        '''
        self.login_user=login_user
        self.member=user
        self.project_id=project_id
        self.role_menu=role_menu
        self.selected_member=selected_member
    
    
    def member_name(self):
        result=self.member.username
        if self.member.last_name and self.member.first_name:
            result=self.member.last_name+self.member.first_name
        return result
    
    def member_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        try:
            if self.member.extend_info:
                result=AccountService.get_avatar_url(self.member)
        except Exception as ex:
            SimpleLogger.exception(ex)   
        return result
    
    def is_member(self):
        result=""
        project_members=ProjectMember.objects.get_members(self.project_id)
        if len(project_members):
            member_ids=[member.PMMember for member in project_members]
            if self.member.id in member_ids:
                result="fa-check"
            else:
                result=""
        return result
    
    
    
    def is_me(self):
        if self.login_user.id==self.member.id:
            return True
        else:
            return False
    
    def role_name(self):
        result="User"
        member=ProjectMember.objects.get_members(self.project_id).filter(PMMember=self.member.id)
        result=ProjectRole.objects.get(member[0].PMRoleID).PRName
        return result
    
    def member_role(self):
        result=1
        member=ProjectMember.objects.get_members(self.project_id).filter(PMMember=self.member.id)
        if len(member):
            result= member[0].PMRoleID
        return result
    
    def is_selected(self):
        result=""
        if isinstance(self.selected_member,list):
            if self.member.id in self.selected_member:
                result="selected"
        else:
            if self.member.id==self.selected_member:
                result="selected"
        return result
    
    def selected_style(self):
        if self.member.id==self.selected_member:
            return "fa-check"
        else:
            return ""
        
    
            
        
        