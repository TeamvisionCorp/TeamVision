#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from teamvision.project.models import WebHook
from django.contrib.auth.models import User

class VM_WebHook(object):
    '''
    classdocs
    '''


    def __init__(self,project_id,webhook,login_user):
        '''
        Constructor
        '''
        self.login_user=login_user
        self.webhook=webhook
        self.project_id=project_id
    
    def category_name(self):
        return "构建"
    
    def is_create(self):
        if self.webhook.WHProjectID:
            return False
        else:
            return True
        
    
            
        
        