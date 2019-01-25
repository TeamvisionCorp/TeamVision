#coding=utf-8
#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from django.db import models
from django.contrib.admin.models import DELETION,CHANGE,ContentType,ADDITION
from doraemon.auth_extend.user.models import ActionLog

class ModelManager(models.Manager):
    '''
    classdocs
    '''
    use_in_migrations = True
    
    def log_action(self,userid,objectid,object_title,action_flag,change_message,projectid,action_type=0):
        log=ActionLog()
        log.ActionFlag=action_flag
        log.ChangeMessage=change_message
        log.ContentType=ContentType.objects.get_for_model(self.model).id
        log.ObjectID=objectid
        log.ObjectRepr=repr(object_title)
        log.User=userid
        log.ProjectID=projectid
        log.ActionType=action_type
        log.save();