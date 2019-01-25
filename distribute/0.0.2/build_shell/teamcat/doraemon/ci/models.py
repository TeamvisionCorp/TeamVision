#coding=utf-8
'''
Created on 2013-12-31

@author: zhangtiande
'''
from django.db import models
from model_managers import ci_model_manager
from doraemon.settings import MONGODB
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
    TaskConfig=models.CharField(default='',max_length=50)
    DeployService=models.IntegerField(default=0)
    TaskHistory=models.IntegerField(default=0)
    Tags=models.CharField(max_length=50,null=True)
    LastRunTime=models.DateTimeField(null=True)
    Schedule=models.CharField(max_length=30,null=True)
    Creator=models.IntegerField(default=0)
    Description=models.CharField(max_length=500,null=True)
    BuildVersion=models.IntegerField(default=0)
    HistoryCleanStrategy=models.IntegerField(default=10)
    LastHistory = models.IntegerField(default=0)
    objects=ci_model_manager.CITaskManager()
    class Meta:
        app_label="ci"
        db_table="ci_task"


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
    CITaskID=models.IntegerField()
    StartTime=models.DateTimeField(null=True)
    EndTime=models.DateTimeField(null=True)
    Tags=models.CharField(max_length=50,null=True)
    PackageID=models.CharField(max_length=500,null=True)
    LogFileID=models.CharField(max_length=500,null=True)
    ChangeLog=models.CharField(max_length=1000,null=True)
    BuildStatus=models.IntegerField()
    BuildLogID=models.IntegerField(default=0)
    TaskQueueID=models.IntegerField()
    TaskUUID=models.CharField(max_length=255,null=True)
    BuildMessage=models.CharField(max_length=255,null=True,blank=True)
    BuildErrorCode=models.IntegerField(default=0,null=True)
    CodeVersion=models.CharField(max_length=255,null=True)
    StartedBy=models.IntegerField()
    BuildVersion=models.IntegerField()
    ProjectVersion=models.IntegerField()
    PackageInfo=models.CharField(max_length=255,null=True)
    BuildParameterID=models.CharField(max_length=30,null=True)
    AgentID=models.IntegerField(default=0)
    FlowSectionHistory=models.IntegerField()
    objects=ci_model_manager.CITaskHistoryManager()
    class Meta:
        app_label="ci"
        db_table="ci_task_history"

class AutoTestingTaskResult(CIModel):
    TaskHistoryID=models.IntegerField()
    Total=models.IntegerField(default=0,null=True)
    Pass=models.IntegerField(default=0,null=True)
    Fail=models.IntegerField(default=0,null=True)
    Aborted=models.IntegerField(default=0,null=True)
    TaskUUID=models.CharField(max_length=128)
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

class CITaskConfig(object):
    
    def __init__(self):
        self.task_name=""
        self.basic_section=BasicSection().__dict__
        self.pre_section=PreBuildSection().__dict__
        self.scm_section=SCMSection().__dict__
        self.build_section=BuildSection().__dict__
        self.post_section=PostBuildSection().__dict__
    DB=MONGODB['default']['DB']
    PORT=MONGODB['default']['PORT']
    HOST=MONGODB['default']['HOST']
    objects=ci_model_manager.CITaskConfigManager(HOST,PORT,DB,"ci_task_config")
        

class CITaskSection(object):
    
    def __init__(self):
        self.plugins=list()
    
    
class BasicSection(CITaskSection):
    
    def __init__(self):
        CITaskSection.__init__(self)
        self.section_id=0

class PreBuildSection(CITaskSection):
    def __init__(self):
        CITaskSection.__init__(self)
        self.section_id=1

class SCMSection(CITaskSection):
    def __init__(self):
        CITaskSection.__init__(self)
        self.section_id=2
    
class BuildSection(CITaskSection):
    def __init__(self):
        CITaskSection.__init__(self)
        self.section_id=3
    
class PostBuildSection(CITaskSection):
    def __init__(self):
        CITaskSection.__init__(self)
        self.section_id=4


class TaskConfigPlugin(object):
    order=0
    is_enable=1

class SvnPlugin(TaskConfigPlugin):

    def __init__(self):
        self.plugin_id=1
        self.plugin_name=CITaskPlugin.objects.get(self.plugin_id).PluginName
        self.remote_url=""
        self.local_dir=""
        self.credentials=0
        self.version="HEAD"

class GitPlugin(TaskConfigPlugin):
    
    def __init__(self):
        self.plugin_id=2
        self.plugin_name=CITaskPlugin.objects.get(self.plugin_id).PluginName
        self.remote_url=""
        self.local_dir=""
        self.credentials=0
        self.version="HEAD"
        self.branch="master"
    
    
    
    





    