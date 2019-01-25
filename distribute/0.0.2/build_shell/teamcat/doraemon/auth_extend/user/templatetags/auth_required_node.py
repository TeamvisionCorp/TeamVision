#coding=utf-8
'''
Created on 2016-1-19

@author: Devuser
'''
from django import template
from doraemon.auth_extend.user.datamodels.user_group_enum import UserGroupEnum
from business.auth_user.system_role_service import SystemRoleService


class AuthRequiredNode(template.Node):
    
    def is_authed(self,context,auth_group):
        result=False
        request=context['request']
        current_group=SystemRoleService.get_role(auth_group)
        for group in request.user.groups.all():
            if group.extend_info.group_priority<=current_group.extend_info.group_priority:
                result=True
                break
        return result



class LoginRequiredNode(AuthRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        request=context['request']
        if request.user.is_authenticated:
            result=output
        return result


class LogoutRequiredNode(AuthRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        request=context['request']
        if not request.user.is_authenticated:
            result=output
        return result
        
    

class AdminRequiredNode(AuthRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context,UserGroupEnum.Group_Admin):
            result=output
        return result

class ManagerRequiredNode(AuthRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context,UserGroupEnum.Grouo_Manager):
            result=output
        return result

class UserRequiredNode(AuthRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context,UserGroupEnum.Group_User):
            result=output
        return result