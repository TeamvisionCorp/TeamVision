#coding=utf-8
'''
Created on 2016-8-24

@author: Devuser
'''
from business.auth_user.user_service import UserService

class VM_ProjectMember(object):
    '''
    classdocs
    '''


    def __init__(self,user_id):
        '''
        Constructor
        '''
        self.user_id=user_id
        self.user_name=self.get_member().last_name+self.get_member().first_name
        self.email=self.get_member().email       
        
    def get_member(self):
        user=UserService.get_user(int(self.user_id))
        return user
        