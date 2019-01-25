#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models
from model_managers import project_model_manager
from markdownx.models import MarkdownxField
from bson.json_util import default
from model_managers import home_model_manager
from doraemon.settings import MONGODB



class ENVModel(models.Model):
    CreationTime=models.DateTimeField(auto_now=True)
    IsActive=models.BooleanField(default=True)
    
    class Meta:
        abstract=True



class issue(ENVModel):
    TProjectID=models.IntegerField()
    TTitle=models.CharField(max_length=255)
    TDeadLine=models.DateField(null=True)
    TStartDate=models.DateField(null=True)
    TFinishedDate=models.DateField(null=True)
    TWorkHours=models.IntegerField()
    TOwner=models.CharField(max_length=50)
    TCreator=models.IntegerField()
    TProgress=models.IntegerField()
    TDescription=models.CharField(max_length=1000,null=True)
    TTags=models.CharField(max_length=50,null=True)
    TStatus=models.IntegerField()
    objects=project_model_manager.TaskManager()
    
    class Meta:
        app_label="issue"
        db_table="issue_task"


    