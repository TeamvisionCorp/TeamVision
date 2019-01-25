#coding=utf-8
'''
Created on 2016-8-24

@author: zhangtiande
'''
from business.auth_user.user_service import UserService
from teamvision.project.models import Task

class ApiProjectTask(Task):
    '''
    classdocs
    '''


    def __init__(self,task_id):
        '''
        Constructor
        '''
        self.Child=task_id.Children.all().filter(Parent=task_id.id)
        
    def get_member(self):
        user=UserService.get_user(int(self.user_id))
        return user
        