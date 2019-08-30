#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from teamvision.auth_extend.user.models import ActionLog

class LogActionService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def project_actions(project_id):
        return ActionLog.objects.all().filter(ProjectID=project_id).order_by('-id')

    @staticmethod
    def all_project_actions(project_ids):
        return ActionLog.objects.all().filter(ProjectID__in=project_ids).order_by('-id')
        
    
    