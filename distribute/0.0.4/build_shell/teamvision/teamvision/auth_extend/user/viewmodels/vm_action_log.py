#coding=utf-8
'''
Created on 2015-11-18

@author: Devuser
'''

from django.contrib.auth.models import User
from teamvision.project.models import Project
from gatesidelib.datetimehelper import DateTimeHelper
from business.ucenter.account_service import AccountService
from business.common.system_config_service import SystemConfigService
import datetime
from teamvision.gatesidelib.common.simplelogger import SimpleLogger

class VM_ActionLog(object):
    '''
    classdocs
    '''


    def __init__(self,action_log,is_fullpart,login_user):
        '''
        Constructor
        '''
        self.user=login_user
        self.action_log=action_log
        self.is_fullpart=is_fullpart
    
    
    def user_name(self):
        result="系统任务"
        try:
            action_user=User.objects.get(id=self.action_log.User)
            result=action_user.username
            if action_user.last_name and action_user.first_name:
                result=action_user.last_name+action_user.first_name
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def action_time(self):
        now= datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        action_time=datetime.datetime.strptime(self.action_log.ActionTime.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        action_time=action_time + datetime.timedelta(hours=8)
        time_internal=(now-action_time).total_seconds()
        return DateTimeHelper.how_long_ago(time_internal)
    
    
    def action_title(self):
        return self.action_log.ObjectRepr
    
    def action_project(self):
        if self.action_log.ProjectID<0:
            return SystemConfigService.get_noproject_name(self.action_log.ProjectID)
        else:
            project=Project.objects.get(self.action_log.ProjectID)
            return project.PBTitle
        
    
    def user_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        try:
            action_user=User.objects.get(id=self.action_log.User)
            if action_user.extend_info:
                result=AccountService.get_avatar_url(action_user)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
        
    
            