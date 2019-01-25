# coding=utf-8
# coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models
from model_managers import project_model_manager
from doraemon.gatesidelib.common.simplelogger import SimpleLogger


class ProjectModel(models.Model):
    CreationTime = models.DateTimeField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)

    class Meta:
        abstract = True


class IssueConfigModel(models.Model):
    IsActive = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Task(ProjectModel):
    ProjectID = models.IntegerField()
    Title = models.CharField(max_length=255)
    DeadLine = models.DateField(null=True)
    StartDate = models.DateField(null=True)
    FinishedDate = models.DateField(null=True)
    WorkHours = models.IntegerField()
    Owner = models.CharField(max_length=50)
    Creator = models.IntegerField()
    Progress = models.IntegerField()
    Description = models.CharField(max_length=1000, null=True)
    Tags = models.CharField(max_length=50, null=True)
    Status = models.IntegerField()
    Parent = models.ForeignKey('self', null=True, db_column='Parent', related_name='Children',on_delete=models.CASCADE)
    Priority = models.IntegerField(default=1)
    Version = models.IntegerField(default=0)
    objects = project_model_manager.TaskManager()
    class Meta:
        app_label = "project"
        db_table = "project_task"


class Version(ProjectModel):
    VProjectID = models.IntegerField()
    VVersion = models.CharField(max_length=50)
    VStartDate = models.DateField(null=True)
    VReleaseDate = models.DateField(null=True)
    VDescription = models.CharField(max_length=1000)
    objects = project_model_manager.VersionManager()

    class Meta:
        app_label = "project"
        db_table = "project_version"


class TestApplication(ProjectModel):
    ProjectID = models.IntegerField()
    VersionID = models.IntegerField()
    Topic = models.CharField(null=True, max_length=200)
    Commitor = models.IntegerField(default=0)
    TestingFeature = models.CharField(max_length=2000)
    TestingAdvice = models.CharField(max_length=2000)
    Attachment = models.CharField(null=True, max_length=50)
    CommitTime = models.DateTimeField(null=True)
    Status = models.IntegerField()
    EmailNotificationStatus = models.CharField(max_length=20, default="0,0,0,0,0")
    Testers = models.CharField(max_length=100, default="0,0")
    ExpectCommitDate = models.DateTimeField(null=True)
    TestingDeadLineDate = models.DateTimeField(null=True)
    TestingFinishedDate = models.DateTimeField(null=True)
    ProjectModuleID = models.IntegerField(default=0)
    ProjectCode = models.IntegerField(default=0)
    Creator = models.IntegerField(default=0)
    TestingStartDate = models.DateTimeField(null=True)
    objects = project_model_manager.TestApplicationManager()

    class Meta:
        app_label = "project"
        db_table = "project_test_application"


class ProjectCodeUrl(ProjectModel):
    ApplicationID = models.IntegerField()
    CodeRepertory = models.CharField(max_length=500, null=True)
    Branch = models.CharField(max_length=255, null=True)
    objects = project_model_manager.CodeUrlManager()

    class Meta:
        app_label = "project"
        db_table = "project_code_url"


class WebHook(ProjectModel):
    WHProjectID = models.IntegerField()
    WHURL = models.CharField(max_length=500)
    WHParameters = models.CharField(max_length=500, null=True)
    WHLabel = models.CharField(max_length=50, null=True)
    WHIsDefault = models.BooleanField(default=False)
    WHCatagory = models.IntegerField()
    WHCreator = models.IntegerField()
    objects = project_model_manager.WebHookManager()

    class Meta:
        app_label = "project"
        db_table = "project_webhook"


class ProjectMember(ProjectModel):
    PMProjectID = models.IntegerField()
    PMRoleID = models.IntegerField()
    PMRoleType = models.IntegerField()
    PMMember = models.IntegerField()
    objects = project_model_manager.MemberManager()

    class Meta:
        app_label = "project"
        db_table = "project_member"


class Project(ProjectModel):
    PBTitle = models.CharField(max_length=100)
    PBKey = models.CharField(max_length=10)
    PBDescription = models.CharField(max_length=255, null=True)
    PBVisiableLevel = models.IntegerField()
    PBPlatform = models.IntegerField()
    PBHttpUrl = models.CharField(max_length=255, null=True)
    PBLead = models.IntegerField()
    PBAvatar = models.CharField(max_length=255, null=True)
    Product = models.IntegerField()
    PBCreator = models.IntegerField()
    objects = project_model_manager.ProjectManager()

    class Meta:
        app_label = "project"
        db_table = "project"


class Product(ProjectModel):
    PTitle = models.CharField(max_length=100)
    PKey = models.CharField(max_length=10)
    PDescription = models.CharField(max_length=255, null=True)
    PVisiableLevel = models.IntegerField()
    LabelColor = models.CharField(max_length=25, null=True)
    objects = project_model_manager.ProductManager()

    class Meta:
        app_label = "project"
        db_table = "product"


class ProjectModule(ProjectModel):
    Name = models.CharField(max_length=100)
    ProjectID = models.IntegerField()
    Description = models.CharField(max_length=255, null=True)
    objects = project_model_manager.ModuleManager()

    class Meta:
        app_label = "project"
        db_table = "project_module"


class Tag(ProjectModel):
    TagName = models.CharField(max_length=20)
    TagProjectID = models.IntegerField()
    TagColor = models.CharField(max_length=50, null=True)
    TagAvatar = models.CharField(max_length=255, null=True)
    TagType = models.IntegerField(default=1)
    TagVisableLevel = models.IntegerField()
    TagOwner = models.IntegerField()
    objects = project_model_manager.TagManager()

    class Meta:
        app_label = "project"
        db_table = "project_tag"


class ProjectRole(ProjectModel):
    PRName = models.CharField(max_length=20)
    PRColor = models.CharField(max_length=50, null=True)
    PRAuthGroup = models.IntegerField()
    PRRoleDesc = models.CharField(max_length=500, null=True)
    objects = project_model_manager.RoleManager()

    class Meta:
        app_label = "project"
        db_table = "project_role"


class ProjectArchive(ProjectModel):
    VersionID = models.IntegerField()
    ProjectID = models.CharField(max_length=50, null=True)
    HistoryID = models.IntegerField()
    Archives = models.CharField(max_length=500, null=True)
    objects = project_model_manager.ArchiveManager()

    class Meta:
        app_label = "project"
        db_table = "project_archive"


class ProjectIssue(ProjectModel):
    issue_desc_default = "​<br/>​步骤：<br/>​实际结果：<br/>​期望结果：<br/>​备注：<br/>"
    Project = models.IntegerField()
    Version = models.IntegerField(verbose_name="版本号")
    Status = models.IntegerField(verbose_name="问题状态")
    Processor = models.IntegerField(verbose_name="问题经办人")
    Solver = models.IntegerField(verbose_name="问题解决者")
    Creator = models.IntegerField(verbose_name="问题创建人")
    Severity = models.IntegerField(verbose_name="问题严重性")
    Solution = models.IntegerField(verbose_name="问题解决结果")
    Title = models.CharField(max_length=500, verbose_name="问题标题")
    Desc = models.CharField(max_length=2000, null=True, default=issue_desc_default, verbose_name="问题描述")
    Module = models.IntegerField(verbose_name="问题模块")
    ProjectPhase = models.IntegerField(verbose_name="项目阶段")
    IssueCategory = models.IntegerField(verbose_name="问题类别")
    DeviceOS = models.IntegerField(default=0, verbose_name="设备系统")
    OSVersion = models.IntegerField(default=0, verbose_name="设备系统版本")
    Attachments = models.CharField(max_length=500, null=True, verbose_name="附件")
    ResolvedTime = models.DateTimeField(null=True, verbose_name="解决结果")
    ClosedTime = models.DateTimeField(null=True)
    ReopenCounts = models.IntegerField(default=0)
    UpdateTime = models.DateTimeField(null=True)
    Team = models.IntegerField(default=0)
    objects = project_model_manager.IssueManager()

    class Meta:
        app_label = "project"
        db_table = "project_issue"

    def get_field_verbose_name(self, field_name):
        result = ""
        try:
            result = ProjectIssue._meta.get_field(field_name).verbose_name
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_field_name(self, field_name):
        return ProjectIssue._meta.get_field(field_name).name


class ProjectIssueDailyStatistics(ProjectModel):
    ProjectID = models.IntegerField()
    StatisticsDate = models.DateField()
    OpenedTotal = models.IntegerField()
    ClosedTotal = models.IntegerField()
    FixedTotal = models.IntegerField()
    OpenedToday = models.IntegerField()
    FixedToday = models.IntegerField()
    ReopenedToday = models.IntegerField()
    VersionID = models.IntegerField()
    objects = project_model_manager.IssueDailyStatisticsManager()

    class Meta:
        app_label = "project"
        db_table = "issue_daily_statistics"


class ProjectIssueVersionStatistics(ProjectModel):
    ProjectID = models.IntegerField()
    VersionID = models.IntegerField()
    StatisticsDate = models.DateField()
    IssueTotal = models.IntegerField()
    DimensionValue = models.IntegerField()
    Dimension = models.IntegerField()
    VersionID = models.IntegerField()
    objects = project_model_manager.IssueVersionStatisticsManager()

    class Meta:
        app_label = "project"
        db_table = "issue_version_statistics"

    class DimensionType:
        Severity = 1
        Category = 2
        ResolvedType = 3
        Module = 4


class IssueActivity(ProjectModel):
    Issue = models.IntegerField()
    OldValue = models.CharField(max_length=2500, null=True)
    NewValue = models.CharField(max_length=2500, null=True)
    FieldName = models.CharField(max_length=20, null=True)
    FieldDesc = models.CharField(max_length=50, null=True)
    ActionType = models.IntegerField()
    ActionFlag = models.IntegerField()
    Creator = models.IntegerField()
    Message = models.CharField(max_length=2500, null=True)
    objects = project_model_manager.IssueActivityManager()

    class Meta:
        app_label = "project"
        db_table = "issue_activity"


class IssueFilter(ProjectModel):
    Project = models.IntegerField()
    Creator = models.IntegerField()
    Scope = models.IntegerField(default=1)
    FilterName = models.CharField(max_length=50)
    FilterString = models.CharField(max_length=500, null=True)
    FilterUIConfig = models.CharField(max_length=500, null=True)
    FilterCacheString = models.CharField(max_length=500, null=True)
    objects = project_model_manager.IssueFilterManager()

    class Meta:
        app_label = "project"
        db_table = "issue_filter"


class ProjectIssueStatus(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    Project = models.IntegerField()
    LabelStyle = models.CharField(max_length=50, null=True)
    Label = models.CharField(max_length=50, null=True)
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_issue_status"


class ProjectIssueResolvedResult(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    Project = models.IntegerField()
    LabelStyle = models.CharField(max_length=50, null=True)
    Label = models.CharField(max_length=50, null=True)
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_issue_resolved_result"


class ProjectIssueSeverity(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    Project = models.IntegerField()
    LabelStyle = models.CharField(max_length=50, null=True)
    Label = models.CharField(max_length=50, null=True)
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_issue_severity"


class ProjectPhase(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_phase"


class ProjectOS(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_os"


class ProjectOSVersion(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    OS = models.IntegerField()
    objects = project_model_manager.ProjectOSVersionManager()

    class Meta:
        app_label = "project"
        db_table = "project_os_version"


class ProjectIssueCategory(IssueConfigModel):
    Value = models.IntegerField()
    Name = models.CharField(max_length=50, null=True)
    Desc = models.CharField(max_length=100, null=True)
    Project = models.IntegerField()
    objects = project_model_manager.IssueConfigFieldManager()

    class Meta:
        app_label = "project"
        db_table = "project_issue_category"
