# coding=utf-8
'''
Created on 2016-8-24

@author: zhangtiande
'''
from business.auth_user.user_service import UserService
from doraemon.project.models import Project,Version,ProjectMember
from doraemon.api.project.viewmodel.api_project_member import ApiProjectMember


class ApiProject(Project):
    '''
    classdocs
    '''

    def __init__(self, project):
        '''
        Constructor
        '''
        self.project = project
        self.Versions=[]
        self.Members=[]

    def get_versions(self):
        versions=Version.objects.get_versions(self.project.id).order_by('-id')
        return versions

    def get_members(self):
        members=ProjectMember.objects.get_members(self.project.id)
        for member in members:
            temp=ApiProjectMember(member)
            member=temp.get_object()
        return members

    def get_object(self,show_extinfo=0):
        if str(show_extinfo) == '1':
            self.Versions=self.get_versions()
            self.Members=self.get_members()
        self.project.Versions=self.Versions
        self.project.Members=self.Members
        return self.project
