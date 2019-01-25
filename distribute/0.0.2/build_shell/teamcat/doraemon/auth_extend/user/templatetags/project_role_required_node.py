#coding=utf-8
'''
Created on 2016-1-19

@author: Devuser
'''
from django import template
from doraemon.project.datamodels.project_role_enum import ProjectRoleEnum
from doraemon.project.models import ProjectMember


class ProjectRoleRequiredNode(template.Node):
    
    def is_authed(self,context,project_paras,role_id):
        result=False
        if str(project_paras)=="0":
            result=True
        else:
            project_id=self.get_project_id(context,project_paras)
            request=context['request']
            member=ProjectMember.objects.get_member(int(project_id),request.user.id)
            if not member==None:
                if member.PMRoleID==role_id:
                    result=True
                if member.PMRoleID==ProjectRoleEnum.Owner:
                    result=True
                if member.PMRoleID==ProjectRoleEnum.Admin:
                    result=True      
        return result
    
    def get_project_id(self,context,project_paras):
        parameters=project_paras.split('.')
        if len(parameters)<2:
                project_id=context[parameters[0]]
        else:
                project_object=context[parameters[0]]
                for parameter in parameters[1:]:
                    project_object=self.get_project_object(project_object, parameter)
                if project_object:
                    project_id=project_object
        return project_id
    
    def get_project_object(self,parent_object,attr_name):
        return parent_object.__getattribute__(attr_name)
        



class TesterRequiredNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context, self.project_id,ProjectRoleEnum.Tester):
            result=output
        return result


class DevRequiredNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context, self.project_id,ProjectRoleEnum.Dev):
            result=output
        return result
        
    

class AdminRequiredNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context, self.project_id,ProjectRoleEnum.Admin):
            result=output
        return result

class ManagerRequiredNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context, self.project_id,ProjectRoleEnum.Owner) or self.is_authed(context, self.project_id,ProjectRoleEnum.Admin):
            result=output
        return result
    
class OwnerRequiredNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        if self.is_authed(context, self.project_id,ProjectRoleEnum.Owner):
            result=output
        return result


class UserNotAllowedNode(ProjectRoleRequiredNode):
    '''
    classdocs
    '''
    def __init__(self, nodelist,project_id):
        self.nodelist = nodelist
        self.project_id=project_id
    
    def render(self, context):
        result=""
        output = self.nodelist.render(context)
        project_id=self.get_project_id(context,self.project_id)
        request=context['request']
        member=ProjectMember.objects.get_member(int(project_id),request.user.id)
        if member:
            if member.PMRoleID!=ProjectRoleEnum.User:
                result=output
        return result