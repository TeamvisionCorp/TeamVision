#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

# from dataaccess.common.dal_dictvalue import DAL_DictValue
# from business.common.userservice import UserService
# from dataaccess.testjob.dal_testjob import DAL_TestJob
import time
import datetime

class VM_Home(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,loginuser):

        self.user=loginuser
    
    
    def can_view_project(self):
        result=False
        if self.user.has_perm('testjob.view_testproject'):
            result=True
        return result
        
        