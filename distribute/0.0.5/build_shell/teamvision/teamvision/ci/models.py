#coding=utf-8
'''
Created on 2013-12-31

@author: zhangtiande
'''
from django.db import models
from model_managers import ci_model_manager
from teamvision.settings import MONGODB
from bson.json_util import default



class CIModel(models.Model):
    CreateTime=models.DateTimeField(auto_now_add=True)
    IsActive=models.BooleanField(default=1)
    
    class Meta:
        abstract=True

class CITask(CIModel):
    TaskName=models.CharField(max_length=150,null=False)
    Project=models.IntegerField(default=0)
    TaskType=models.IntegerField(default=0)
    LastRunTime=models.DateTimeField(null=True)
    Schedule=models.CharField(max_length=30,null=True)
    Creator=models.IntegerField(default=0)
    Description=models.CharField(max_length=500,null=True)
    BuildVersion=models.IntegerField(default=0)
    HistoryCleanStrategy=models.IntegerField(default=10)
    ExecuteStrategy = models.IntegerField(default=1)
    LastHistory = models.IntegerField(default=0)
    objects=ci_model_manager.CITaskManager()
    class Meta:
        app_label="ci"
        db_table="ci_task"

class CITaskStageHistory(CIModel):
    '''
    Status: 0 未开始执行，1 执行中，2 执行完毕，3 执行取消,4 执行失败
    '''
    TaskID = models.IntegerField()
    Status = models.IntegerField(help_text="Status: 0 未开始执行，1 执行中，2 执行完毕，3 执行取消,4 执行失败")
    StartTime = models.DateTimeField(null=True)
    EndTime = models.DateTimeField(null=True)
    BuildResult = models.IntegerField(null=True)
    BuildMessage = models.CharField(max_length=500,null=True,blank=True)
    TaskHistoryID = models.IntegerField()
    TQUUID = models.CharField(max_length=100,null=True,blank=True)
    StageID = models.CharField(max_length=100,null=True,blank=True)
    objects = ci_model_manager.CITaskStageHistoryManager()
    class Meta:
        app_label="ci"
        db_table="ci_task_stage_history"


class CITaskStepOutput(CIModel):
    '''
    ProductType: 1 buildlog,2 iosfile,3 android fle 4 code change log 5 code version,6 other file
    '''
    StageID = models.CharField(max_length=100,null=True,blank=True)
    TaskID = models.IntegerField()
    StageHistoryID = models.IntegerField()
    TaskHistoryID = models.IntegerField()
    ProductID = models.CharField(max_length=100,null=True,blank=True)
    ProductType = models.IntegerField(help_text="ProductType: 1 buildlog,2 iosfile,3 android fle 4 code change log 5 code version,6 other file,7 gat test result,8 unit test result")
    StepID = models.CharField(max_length=100,null=True,blank=True)
    CodeVersion = models.CharField(max_length=1000,null=True,blank=True)
    PackageInfo = models.CharField(max_length=500,null=True,blank=True)
    ChangeLog = models.TextField(null=True,blank=True)
    objects = ci_model_manager.CITaskStepOutputManager()
    class Meta:
        app_label="ci"
        db_table="ci_task_step_output"


class CITaskFlow(CIModel):
    FlowName=models.CharField(max_length=50,null=False)
    Project=models.IntegerField(default=0)
    LastRunStatus = models.IntegerField(default=1)
    LastRunTime = models.DateTimeField(null=True)
    Creator=models.IntegerField(default=0)
    Description=models.CharField(max_length=500,null=True)
    LastHistory = models.IntegerField(default=0)
    objects=ci_model_manager.CITaskFlowManager()
    class Meta:
        app_label="ci"
        db_table="ci_taskflow"


class CITaskFlowSection(CIModel):
    SectionName = models.CharField(max_length=50,null=False)
    TaskFlow = models.IntegerField()
    SectionOrder = models.IntegerField(null=False)
    CITasks = models.CharField(default='',max_length=200,null=True,blank=True)
    objects = ci_model_manager.CITaskFlowSectionManager()
    class Meta:
        app_label="ci"
        db_table="ci_taskflow_section"

class CITaskFlowHistory(CIModel):
    TaskFlow = models.IntegerField()
    Status = models.IntegerField(default=1)
    StartTime = models.DateTimeField(null=True)
    EndTime = models.DateTimeField(null=True)
    BuildMessage=models.CharField(max_length=255,null=True,blank=True)
    StartedBy = models.IntegerField()
    TQUUID = models.CharField(max_length=500,null=True)
    objects=ci_model_manager.CITaskFlowHistoryManager()
    class Meta:
        app_label="ci"
        db_table="ci_taskflow_history"

class CIFlowSectionHistory(CIModel):
    TaskFlowHistory = models.IntegerField()
    TaskFlow = models.IntegerField()
    Section = models.IntegerField()
    Status = models.IntegerField(default=1)
    StartTime = models.DateTimeField(null=True)
    BuildMessage=models.CharField(max_length=255,null=True,blank=True)
    EndTime = models.DateTimeField(null=True)
    StartedBy = models.IntegerField()
    TQUUID = models.CharField(max_length=500,null=True)
    objects=ci_model_manager.CIFlowSectionHistoryManager()
    class Meta:
        app_label="ci"
        db_table="ci_flowsection_history"


class CITaskHistory(CIModel):
    '''
    Status: 0 未开始执行，1 执行中，2 执行完毕，3 执行取消,4 执行失败
    '''
    CITaskID=models.IntegerField()
    StartTime=models.DateTimeField(null=True)
    EndTime=models.DateTimeField(null=True)
    Status=models.IntegerField(help_text="Status: 0 未开始执行，1 执行中，2 执行完毕，3 执行取消,4 执行失败")
    TaskUUID=models.CharField(max_length=255,null=True)
    StartedBy=models.IntegerField()
    BuildVersion=models.IntegerField()
    ProjectVersion=models.IntegerField()
    BuildParameterID=models.CharField(max_length=30,null=True)
    AgentID=models.IntegerField(default=0,null=True)
    FlowSectionHistory=models.IntegerField(null=True)
    objects=ci_model_manager.CITaskHistoryManager()
    class Meta:
        app_label="ci"
        db_table="ci_task_history"

class AutoTestingTaskResult(CIModel):
    StageHistoryID=models.IntegerField()
    Total=models.IntegerField(default=0,null=True)
    Pass=models.IntegerField(default=0,null=True)
    Fail=models.IntegerField(default=0,null=True)
    Aborted=models.IntegerField(default=0,null=True)
    TaskUUID=models.CharField(max_length=128)
    StepID = models.CharField(max_length=128)
    ParentResultID=models.IntegerField(default=0,null=True)
    RuntimeEnv=models.IntegerField(default=0,null=True)
    AgentID=models.IntegerField(default=0,null=True)
    MobileDeviceID=models.IntegerField(default=0,null=True)
    BuildMessage=models.CharField(max_length=255,null=True,blank=True)
    Status=models.IntegerField()
    objects=ci_model_manager.AutoTaskResultManager()
    class Meta:
        app_label="ci"
        db_table="autotesting_task_result"

class AutoCaseResult(CIModel):
    ''' data model for task run summary result
    '''
    TestCaseID=models.IntegerField()
    TaskResultID=models.IntegerField()
    StartTime=models.DateTimeField(null=True)
    EndTime=models.DateTimeField(null=True)
    Result=models.IntegerField(default=0)
    Error=models.CharField(max_length=1000,null=True)
    StackTrace=models.TextField(null=True)
    BugID=models.IntegerField(default=0)
    FailCategoryID=models.IntegerField(default=0)
    ReRunID=models.IntegerField(default=0)
    FailType=models.IntegerField(default=0)
    FailNote=models.CharField(null=True,max_length=255)
    CaseVersion=models.CharField(max_length=50,null=True)
    objects=ci_model_manager.AutoCaseResultManager()
    class Meta:
        app_label='ci'
        db_table='autotesting_case_result'


class UnitTestCaseResult(CIModel):
    ''' data model for unittest case result
    '''
    TestCaseName=models.CharField(max_length=100,null=True)
    TaskResultID=models.IntegerField(default=0)
    StartTime=models.DateTimeField(null=True)
    EndTime=models.DateTimeField(null=True)
    Result=models.IntegerField(default=0)
    Error=models.CharField(max_length=1000,null=True)
    StackTrace=models.CharField(max_length=5000,null=True)
    BugID=models.IntegerField(default=0)
    FailCategoryID=models.IntegerField(default=0)
    ReRunID=models.IntegerField(default=0)
    FailType=models.IntegerField(default=0)
    FailNote=models.CharField(null=True,max_length=255)
    CaseVersion=models.CharField(max_length=50,null=True)
    objects=ci_model_manager.UnitTestCaseResultManager()
    class Meta:
        app_label='ci'
        db_table='unittest_case_result'
        

# class AutoCase(CIModel):
#     ''' data model for task run summary result
#     '''
#     PackName=models.CharField(max_length=255)
#     ClassName=models.CharField(null=True,max_length=255)
#     CaseName=models.CharField(null=True,max_length=255)
#     Level=models.CharField(null=True,max_length=255)
#     Points=models.CharField(null=True,max_length=255)
#     CaseType=models.IntegerField()
#     CaseGroup=models.CharField(null=True,max_length=255)
#     ProjectID=models.IntegerField()
#     RunCount=models.IntegerField()
#     FailCount=models.IntegerField()
#     FailType=models.IntegerField()
#     FailNote=models.CharField(null=True,max_length=255)
#     objects=ci_model_manager.AutoCaseManager()
#     class Meta:
#         app_label='ci'
#         db_table='autotesting_testcase'


class AutoCase(CIModel):
    ''' data model for task run summary result
    '''
    PackageName=models.CharField(max_length=255)
    ClassName=models.CharField(null=True,max_length=255)
    CaseName=models.CharField(null=True,max_length=255)
    CaseType=models.IntegerField()
    ProjectID=models.IntegerField()
    ModuleID=models.IntegerField(default=0,null=True)
    InterfaceID=models.IntegerField(default=0,null=True)
    CaseTag=models.CharField(max_length=255,null=True)
    Version=models.IntegerField(default=0,null=True)
    Desc=models.CharField(max_length=500,null=True)
    objects=ci_model_manager.AutoCaseManager()
    class Meta:
        app_label='ci'
        db_table='autotesting_testcase'
        

class CaseTag(CIModel):
    ''' data model for case tag
    '''
    TagName=models.CharField(max_length=255)
    TagDesc=models.CharField(null=True,max_length=255)
    objects=ci_model_manager.CaseTagManager()
    class Meta:
        app_label='ci'
        db_table='case_tag'
    
    

    

class ServiceHost(CIModel):
    EnvID=models.IntegerField()
    HostIP=models.CharField(max_length=255)
    HostService=models.CharField(max_length=255)
    Description=models.CharField(null=True,max_length=255)
    objects=ci_model_manager.ServiceHostManager()
    class Meta:
        app_label="ci"
        db_table='ci_servicehost'
        
    
        
        
class CITaskPlugin(CIModel):
    PluginName=models.CharField(max_length=50)
    PluginSection=models.CharField(max_length=50)
    PluginLabelColor=models.CharField(max_length=10)
    Description=models.CharField(max_length=500,null=True)
    TaskType=models.CharField(max_length=50)
    objects=ci_model_manager.CIPluginManager()
    
    class Meta:
        app_label="ci"
        db_table="ci_task_plugin"



class CIDeployService(CIModel):
    ServiceName=models.CharField(max_length=100)
    DeployDir=models.CharField(max_length=500)
    AccessLog=models.CharField(max_length=1000,null=True,default="")
    ErrorLog=models.CharField(max_length=1000,null=True,default="")
    StartCommand=models.CharField(max_length=500,null=True,default="")
    StopCommand=models.CharField(max_length=500,null=True,default="")
    RestartCommand=models.CharField(max_length=500,null=True,default="")
    RelatedFiles=models.CharField(max_length=500,null=True,default="")
    DeployScripts=models.CharField(max_length=500,null=True,default="")
    AdvanceConfig=models.CharField(max_length=50,null=True,default="")
    Project=models.IntegerField()
    objects=ci_model_manager.CIDeployServiceManager()
    
    class Meta:
        app_label="ci"
        db_table="ci_deploy_service"


class CITaskApiTrigger(CIModel):
    '''
    ActionType: 1:start,2 stop
    '''
    TriggerName = models.CharField(max_length=100,default="API")
    TriggerUUID = models.CharField(max_length=500,null=True,blank=True)
    TaskQueueUUID = models.CharField(max_length=100)
    ActionType = models.IntegerField(help_text="ActionType: 1:start,2 stop")
    TaskID = models.IntegerField()
    Branch = models.CharField(max_length=1000, null=True, blank=True)
    CodeAddress = models.CharField(max_length=1000, null=True, blank=True)
    CommitID = models.CharField(max_length=500, null=True, blank=True)
    BuildParameter = models.CharField(max_length=100, null=True, blank=True)
    objects = ci_model_manager.CITaskApiTriggerManager()

    class Meta:
        app_label = "ci"
        db_table = "ci_task_apitrigger"


class CICredentials(CIModel):
    UserName=models.CharField(max_length=100,null=True)
    Password=models.CharField(max_length=100,null=True)
    SSHKey=models.CharField(max_length=1000,null=True,default="")
    Scope=models.IntegerField()
    CredentialType=models.IntegerField(default=1)
    Creator=models.IntegerField()
    Description=models.CharField(max_length=100,null=True)
    objects=ci_model_manager.CICredentialsManager()
    
    class Meta:
        app_label="ci"
        db_table="ci_credentials"

class CIServer(CIModel):
    ServerName=models.CharField(max_length=100)
    Host=models.CharField(max_length=100)
    RemoteDir=models.CharField(max_length=200,null=True)
    Port=models.IntegerField()
    Scope=models.IntegerField()
    Description=models.CharField(max_length=100,null=True)
    Creator=models.IntegerField()
    Credential=models.IntegerField()
    objects=ci_model_manager.CICredentialsManager()
    
    class Meta:
        app_label="ci"
        db_table="ci_server"

    
    
    





    