#coding=utf-8
#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.conf import settings
from django.contrib.auth.models import Group,Permission
from django.db import models
from django.contrib.admin.models import ContentType
from model_managers import user_model_manager



class User_Extend(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="extend_info"
    )
    
    
    avatar=models.CharField(max_length=255,null=True)
    side_bars=models.CharField(max_length=255,null=True)
    dashboard_tools=models.CharField(max_length=255,null=True)
    shortcuts=models.CharField(max_length=255,null=True)
    
    class Meta:
        app_label="user"
        db_table="auth_user_extend"

class UserGroups(models.Model):
    user_id=models.IntegerField()
    group_id=models.IntegerField()
    objects=user_model_manager.UserGroupsManager()
    class Meta:
        app_label="user"
        db_table="auth_user_groups_teamcat"

class User_Group_Extend(models.Model):
    group = models.OneToOneField(Group,
        on_delete=models.CASCADE,
        related_name="extend_info"
    )
    backcolor=models.CharField(max_length=255,null=True)
    description=models.CharField(max_length=255,null=True)
    group_priority=models.IntegerField()
    class Meta:
        app_label="user"
        db_table="auth_group_extend"

class User_Permission_Extend(models.Model):
    permission = models.OneToOneField(Permission,
        on_delete=models.CASCADE,
        related_name="extend_info"
    )
    PermissionType=models.IntegerField()
    Description=models.CharField(max_length=255)
    
    class Meta:
        app_label="user"
        db_table="auth_permission_extend"


class ActionLog(models.Model):
    ActionTime = models.DateTimeField(auto_now=True)
    User= models.IntegerField()
    ContentType = models.IntegerField()
    ObjectID = models.CharField(max_length=255,blank=True, null=True)
    ObjectRepr = models.CharField(max_length=200)
    ActionFlag = models.PositiveSmallIntegerField()
    ChangeMessage = models.CharField(max_length=255,blank=True)
    ActionType=models.IntegerField(default=0)
    ProjectID=models.IntegerField(default=0)
    objects=user_model_manager.ActionLogManager

    class Meta:
        app_label="user"
        db_table="user_action_log"