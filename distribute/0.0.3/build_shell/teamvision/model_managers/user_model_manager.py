#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from django.db import models


class ActionLogManager(models.Manager):
    '''
    classdocs
    '''
    def all(self,projectid):
        return super(ActionLogManager,self).get_queryset()
    
    def get(self,action_id):
        result=None
        try:
            result=super(ActionLogManager,self).get_queryset().get(id=action_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
class UserGroupsManager(models.Manager):
    '''
    classdocs
    '''
    
    def all(self):
        return super(UserGroupsManager,self).get_queryset()
    
    def user_groups(self,user_id):
        return self.all().filter(user_id=user_id)
    
    def get(self,group_id):
        result=None
        try:
            result=super(ActionLogManager,self).get_queryset().get(id=group_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
