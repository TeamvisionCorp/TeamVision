#coding=utf-8
'''
Created on 2016-8-24

@author: zhangtiande
'''
from business.auth_user.user_service import UserService
from doraemon.project.models import ProjectMember

class ApiProjectMember(ProjectMember):
    '''
    classdocs
    '''


    def __init__(self,member):
        '''
        Constructor
        '''
        self.member=member
        self.name=self.get_member().last_name+self.get_member().first_name
        self.email=self.get_member().email

    def get_member(self):
        user=UserService.get_user(int(self.member.PMMember))
        return user

    def get_object(self):
        self.member.email = self.email
        self.member.name = self.name
        return self.member
        