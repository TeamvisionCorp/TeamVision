#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models

class AutoTask(models.Model):
    '''
    data model for automation task
    '''
    TaskName=models.CharField(max_length=255,unique=True,editable=True)
    TaskTestingConfigID=models.IntegerField()
    TaskCaseQuerySet=models.IntegerField()
#     TaskViewScope=models.IntegerField()
#     TaskTpye=models.IntegerField()
    TaskAgentID=models.IntegerField()
    TaskStatus=models.IntegerField()
    TaskLastRunTime=models.DateTimeField(null=True)
    TaskCreationTime=models.DateTimeField(auto_now=True)
    TaskOwner=models.IntegerField()
    TaskIsActive=models.BooleanField(default=True)
    TaskProjectID=models.IntegerField()
    TaskIsSplit=models.BooleanField(default=False)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_task'
        
class AutoTestConfig(models.Model):
    '''
    data model for testing config
    '''
    TCFName=models.CharField(max_length=255,unique=True,editable=True)
    TCFTaskTpye=models.IntegerField()
    TCFCodeURL=models.CharField(max_length=255)
    TCFProjectID=models.IntegerField()
    TCFProjectVersion=models.IntegerField()
    TCFCreationTime=models.DateTimeField(auto_now=True)
    TCFIsActive=models.BooleanField(default=True)
    TCFOS=models.IntegerField(null=True)
    TCFOSVersion=models.CharField(max_length=50,null=True)
    TCFBrowser=models.CharField(max_length=50,null=True)
    TCFTestingEnv=models.IntegerField()
    TCFIsSplit=models.BooleanField(default=False)
    TCFRunTiming=models.CharField(max_length=50,null=True)
    TCFViewScope=models.IntegerField()
    TCFExecuteDriver=models.IntegerField(default=0)
    TCFDriverArgs=models.CharField(max_length=500,null=True)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_config'

class AutoAgent(models.Model):
    '''
    data model for automation agent
    '''
    AName=models.CharField(max_length=255,unique=True)
    AIP=models.CharField(max_length=20)
    AOS=models.IntegerField()
    AStatus=models.IntegerField()
    AAgentWorkSpace=models.CharField(max_length=255)
    AAgentBrowser=models.CharField(max_length=255)
    AIsActive=models.BooleanField(default=True)
    AIsReserved=models.BooleanField(default=False)
    AgentPort=models.IntegerField()
    ACreationTime=models.DateTimeField(auto_now=True)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_agent'



class AutoMobileDevice(models.Model):
    '''
    data model for mobile device
    '''
    MDeviceName=models.CharField(max_length=255)
    MDeviceOS=models.CharField(max_length=255)
    MDOSVersion=models.CharField(max_length=50)
    MDeviceScreen=models.CharField(max_length=255)
    MDeviceAgent=models.IntegerField()
    MDIsActive=models.BooleanField(default=True)
    MDIsSimulator=models.BooleanField(default=False)
    MDeviceStatus=models.IntegerField()
    MDeviceSerialNumber=models.CharField(max_length=50,null=True)
    MDCreationTime=models.DateTimeField(auto_now=True)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_mobiledevice'


class AutoRunResult(models.Model):
    ''' data models for Task run result
    '''
    TRTaskID=models.IntegerField()
    TRTotal=models.IntegerField(default=0)
    TRPass=models.IntegerField(default=0)
    TRFail=models.IntegerField(default=0)
    TRAborted=models.IntegerField(default=0)
    TRStartTime=models.DateTimeField(null=True)
    TREndTime=models.DateTimeField(auto_now=True)
    TRStatus=models.IntegerField()
    TRUUID=models.CharField(max_length=128)
    TRParentResultID=models.IntegerField(default=0)
    TRTaskViewScope=models.IntegerField()
    TRRuntimeEnv=models.CharField(max_length=50,null=True)
    TRError=models.CharField(max_length=255,null=True)
    TRAgentID=models.IntegerField()
    TRProjectVersion=models.IntegerField(default=0)
    TRIsChild=models.BooleanField(default=False)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_taskrun_result'



class AutoCaseResult(models.Model):
    ''' data model for task run summary result
    '''
    ACRTestCaseID=models.IntegerField()
    ACRTestCaseName=models.CharField(max_length=500)
    ACRTaskID=models.IntegerField()
    ACRRunUUID=models.CharField(max_length=128)
    ACRAgentID=models.IntegerField()
    ACRStartTime=models.DateTimeField()
    ACREndTime=models.DateTimeField()
    ACRResult=models.IntegerField()
    ACRError=models.CharField(max_length=1000,null=True)
    ACRStackTrace=models.CharField(max_length=5000,null=True)
    ACRBugID=models.IntegerField(default=0)
    ACRFailCategoryID=models.IntegerField(default=0)
    ACRCaseVersion=models.CharField(max_length=50,null=True)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_case_result'
    

class AutoServiceHost(models.Model):
    '''dtat model for service host list
    '''
    SHostEnvID=models.IntegerField()
    ShostIP=models.IntegerField()
    SHostServiceList=models.CharField(max_length=1000)
    SHostIsActive=models.BooleanField(default=False)
    SHostDescription=models.CharField(max_length=200)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_service_host'
    

class AutoTaskQueue(models.Model):
    '''data model for task queue
    '''
    TQTaskID=models.IntegerField()
    TQStatus=models.IntegerField()
    TQCaseList=models.CharField(max_length=10000,null=True)
    TQPriority=models.IntegerField()
    TQEnqueueTime=models.DateTimeField(auto_now=True)
    TQRerunReportID=models.IntegerField()
    TQRuntimeEnv=models.IntegerField()
    TQTaskUUID=models.CharField(max_length=128)
    TQAgentID=models.IntegerField(null=True)
    TQStartTime=models.DateTimeField(null=True)
    TQTaskEndTime=models.DateTimeField(null=True)
    TQFromName=models.CharField(max_length=100,null=True)
    TQFromIP=models.CharField(max_length=20,null=True)
    TQIsChild=models.BooleanField(default=False)
    TQCommand=models.IntegerField()
    TQMobileDeviceID=models.IntegerField()
    TQIsLocked=models.BooleanField(default=False)
    TQDistributeTimes=models.IntegerField(null=True)
    TQErrorMsg=models.CharField(max_length=255,null=True)
    class Meta:
        app_label='automationtesting'
        db_table='autotesting_task_queue'










