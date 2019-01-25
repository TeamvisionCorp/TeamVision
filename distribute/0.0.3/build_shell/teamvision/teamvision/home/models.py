#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models
from model_managers import home_model_manager


class HomeModel(models.Model):
    CreationTime=models.DateTimeField(auto_now_add=True)
    IsActive=models.BooleanField(default=True)
    
    class Meta:
        abstract=True

class WebApps(HomeModel):
    app_title=models.CharField(max_length=50)
    app_key=models.CharField(max_length=10)
    app_url=models.CharField(max_length=500)
    app_avatar=models.CharField(max_length=255,null=True)
    app_desc=models.CharField(max_length=500,null=True)
    app_visable_level=models.IntegerField()
    app_creator=models.IntegerField()
    objects=home_model_manager.WebappManager()
    class Meta:
        app_label="home"
        db_table="home_webapps"

class Agent(HomeModel):
    '''
    data model for testingcat agent
    '''
    Name=models.CharField(max_length=255,unique=True)
    IP=models.CharField(max_length=20)
    OS=models.IntegerField()
    Status=models.IntegerField()
    AgentWorkSpace=models.CharField(max_length=255)
    AgentTags=models.CharField(max_length=255)
    AgentPort=models.IntegerField()
    objects=home_model_manager.AgentManager()
    Executors=models.IntegerField(default=0)
    RunningExecutors=models.IntegerField(default=0)
    BuildToolsDir=models.CharField(max_length=500,null=True)
    class Meta:
        app_label='home'
        db_table='agent'


class Team(HomeModel):
    '''
    data model for  team
    '''
    Name=models.CharField(max_length=255,unique=True)
    Desc=models.CharField(max_length=255,unique=True)
    Creator=models.IntegerField()
    objects=home_model_manager.TeamManager()
    class Meta:
        app_label='home'
        db_table='team'

class TaskQueue(models.Model):
    '''data model for task queue
    '''
    TaskID=models.IntegerField()
    Status=models.IntegerField()
    TaskType=models.IntegerField()
    CaseList=models.CharField(max_length=10000,null=True)
    Priority=models.IntegerField()
    EnqueueTime=models.DateTimeField()
    RerunReportID=models.IntegerField()
    RuntimeEnv=models.IntegerField()
    TaskUUID=models.CharField(max_length=128)
    AgentID=models.IntegerField()
    StartTime=models.DateTimeField(null=True)
    TaskEndTime=models.DateTimeField(null=True)
    FromName=models.CharField(max_length=100,null=True)
    FromIP=models.CharField(max_length=20,null=True)
    ParentID=models.IntegerField(default=0)
    Command=models.IntegerField()
    MobileDeviceID=models.IntegerField()
    IsLocked=models.BooleanField(default=False)
    LockTime=models.DateTimeField(null=True)
    DistributeTimes=models.IntegerField()
    ErrorMsg=models.CharField(max_length=255,null=True)
    BuildParameterID=models.CharField(max_length=30,null=True)
    objects=home_model_manager.TaskQueueManager()
    class Meta:
        app_label='home'
        db_table='task_queue'



        

class DicType(models.Model):
    ''' data model for dic type table
    '''
    DicTypeName=models.CharField(max_length=50)
    DicTypeValue=models.IntegerField(default=0)
    DicTypeIsActive=models.BooleanField(default=True)
    objects=home_model_manager.DicTypeManager()
    
    class Meta:
        app_label="home"
        db_table='dictype'

class DicData(models.Model):
    ''' data modele for dic data table
    '''
    DicType=models.ForeignKey(DicType,on_delete=models.CASCADE)
    DicDataName=models.CharField(max_length=500)
    DicDataValue=models.IntegerField(default=0)
    DicDataDesc=models.CharField(max_length=500,null=True)
    DicDataIsActive=models.BooleanField(default=True)
    objects=home_model_manager.DicDataManager()
    class Meta:
        app_label="home"
        db_table='dicdata'
        
class ErrorMessage(models.Model):
    ''' data modele for dic data table
    '''
    ErrorType=models.IntegerField()
    ErrorCode=models.IntegerField()
    ErrorName=models.CharField(max_length=25,null=True)
    ErrorMessage=models.CharField(max_length=100,null=True)
    IsActive=models.BooleanField(default=True)
    objects=home_model_manager.ErrorMessageManager()
    class Meta:
        app_label="home"
        db_table='error_message'


class FileInfo(HomeModel):
    FileName=models.CharField(max_length=255,null=True)
    FileUUID=models.CharField(max_length=50,null=True)
    FilePath=models.CharField(max_length=500,null=True)
    FileType=models.IntegerField()
    FileFolder=models.IntegerField()
    FileSuffixes=models.CharField(max_length=10,null=True)
    FileCreator=models.IntegerField()
    FileSize=models.IntegerField(default=0)
    objects=home_model_manager.FileManager()
    
    class Meta:
        app_label="home"
        db_table="file_info"
    