#coding=utf-8
'''
Created on 2015-11-9

@author: Devuser
'''
from teamvision.project.models import Project

from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from business.auth_user.user_service import UserService

from teamvision.gatesidelib.common.simplelogger import SimpleLogger

class VM_IssueActivity(object):
    



    def __init__(self,activity):
        '''
        Constructor
        '''
        self.activity=activity
        
    def project_title(self):
        dm_project=Project.objects.get(self.activity.Project)
        return dm_project.PBTitle

        
    
    
    def creator_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        try:
            creator=User.objects.get(id=self.fortesting.Creator)
            if creator.extend_info:
                result=AccountService.get_avatar_url(creator)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def creator_name(self):
        creator=User.objects.get(id=self.activity.Creator)
        result=creator.username
        if creator.first_name and creator.last_name:
            result=creator.last_name+creator.first_name
        return result
    
    
    def activity_message(self):
        result=""
        if self.activity.FieldName!="Desc":
            result=self.activity.Message
        return result
            
        
    
    
    
    def create_date(self):
        result="--"
        if self.activity.CreationTime:
            result=self.activity.CreationTime
        return result
    
    def action_type_name(self):
        result=""
        if self.activity.ActionType==1:
            result="问题"
        if self.activity.ActionType==2:
            result="备注"
        return result
        
    
    def action_flag_icon(self):
        result="fa-plus"
        if self.activity.ActionFlag==1:
            result="fa-plus"
        
        if self.activity.ActionFlag==2:
            result="fa-edit" 
        
        if self.activity.ActionFlag==3:
            result="fa-trash-o"
        return result    
    
    def action_flag_name(self):
        result=""
        if self.activity.ActionFlag==1:
            result="添加"
        
        if self.activity.ActionFlag==2:
            result="修改" 
        
        if self.activity.ActionFlag==3:
            result="删除"
        return result    
    