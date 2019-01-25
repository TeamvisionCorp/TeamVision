# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from django.contrib.auth.models import User
from teamvision.project.models import ProjectModule,ProjectOS,ProjectIssuePriority, ProjectIssueStatus, Version, ProjectModule, ProjectIssue, \
    ProjectIssueCategory, ProjectIssueResolvedResult, ProjectIssueSeverity, Product,Project,ProjectPhase
from teamvision.project import models
from teamvision.settings import WEB_HOST,TIME_ZONE
from teamvision.home.models import FileInfo
from teamvision.api.project.viewmodel.api_project_task import ApiProjectTask
from teamvision.api.project.viewmodel.api_project_member import ApiProjectMember
from teamvision.api.project.viewmodel.api_project import ApiProject
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.api.common.serializer.file_serializer import FileSerializer
from teamvision.home.models import Team
from gatesidelib.common.simplelogger import SimpleLogger
from business.auth_user.user_service import UserService
from business.project.task_service import TaskService
from business.ucenter.account_service import AccountService
import datetime,re,time,pytz


class ProjectMemberSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = ApiProjectMember
        exclude = ('CreationTime', 'IsActive')
        read_only_fields = ('id', 'email', 'name')


class ProjectModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModule
        exclude = ('CreationTime', 'IsActive')


class ProjectVersionSerializer(serializers.ModelSerializer):
    VersionLabel = serializers.SerializerMethodField()

    def get_VersionLabel(self, obj):
        result = obj.VVersion
        if obj.VStartDate and obj.VReleaseDate:
            result = result + " ( " + str(obj.VStartDate)[5:] + ':' + str(obj.VReleaseDate)[5:] + " )"
        return result

    class Meta:
        model = Version
        exclude = ('CreationTime', 'IsActive')
        read_only_fields = ('id',)


class IssueActivitySerializer(serializers.ModelSerializer):
    action_flag_name = serializers.SerializerMethodField()
    action_type_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    create_date = serializers.SerializerMethodField()
    FieldDesc = serializers.SerializerMethodField()

    def get_action_flag_name(self,obj):
        result = ''
        if obj.ActionFlag == 1:
            result = "添加了"

        if obj.ActionFlag == 2:
            result = "更新了"

        if obj.ActionFlag == 3:
            result = "删除了"
        return result

    def get_action_type_name(self, obj):
        result = ''
        if obj.ActionType == 1:
            result = "问题"

        if obj.ActionType == 2:
            result = "备注"

        return result

    def get_creator_name(self,obj):
        processor = User.objects.get(id=obj.Creator)
        result = processor.username
        if processor.first_name and processor.last_name:
            result = processor.last_name + processor.first_name
        return result

    def get_create_date(self,issue):
        result = "--"
        if issue.CreationTime:
            result = issue.CreationTime.astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
        return result

    def get_FieldDesc(self,obj):
        result = ''
        if obj.FieldName != '':
            issue = ProjectIssue()
            result = issue.get_field_verbose_name(obj.FieldName)
        return result






    class Meta:
        model = models.IssueActivity
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    Versions = ProjectVersionSerializer(many=True, read_only=True)
    Members = ProjectMemberSerializer(many=True, read_only=True)
    Display = serializers.SerializerMethodField()

    class Meta:
        model = ApiProject
        exclude = ('CreationTime', 'IsActive')
        read_only_fields = ('id', 'Versions', 'Members')

    def get_Display(self, obj):
        return True


class ProjectIssueSerializer(serializers.ModelSerializer):
    project_title = serializers.SerializerMethodField()
    default_title = serializers.SerializerMethodField()
    os_name = serializers.SerializerMethodField()
    version_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    issue_temp_id = serializers.SerializerMethodField()
    severity_name = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    project_phrase_name = serializers.SerializerMethodField()
    solution_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    processor_name = serializers.SerializerMethodField()
    create_date = serializers.SerializerMethodField()
    update_date = serializers.SerializerMethodField()
    priority_name = serializers.SerializerMethodField()
    attachments_detail = serializers.SerializerMethodField()


    def get_project_title(self,issue):
        dm_project = Project.objects.get(issue.Project)
        return dm_project.PBTitle

    def get_default_title(self,issue):
        if str(issue.Team):
            default_title = "[" + self.get_priority_name(issue) + " " + self.get_team_name(issue) + " " + self.get_project_title(issue) + " " + self.get_version_name(issue) + " " + self.get_module_name(issue) + "]"
        return default_title

    def get_os_name(self,issue):
        result = " "
        try:
            if issue.DeviceOS:
                result = models.ProjectOS.objects.get_byvalue(issue.DeviceOS).Name
        except Exception as ex:
            SimpleLogger.exception(ex)

        return result

    def get_module_name(self,issue):
        result = " "
        if issue.Module:
            dm_module = ProjectModule.objects.get(issue.Module)
            result = dm_module.Name
        return result

    def get_team_name(self,issue):
        result = ""
        if issue.Team:
            dm_team = Team.objects.get(issue.Team)
            result = dm_team.Name
        return result

    def get_version_name(self,issue):
        result = ""
        dm_version = Version.objects.get(issue.Version)
        if dm_version:
            result = dm_version.VVersion
        return result

    def get_issue_temp_id(self,user):
        return str(user.id) + "_" + str(time.time())

    def get_severity_name(self,issue):
        result = dict()
        severity  = ProjectIssueSeverity.objects.get_byvalue(issue.Severity)
        if severity:
            severity_serializer = ProjectIssueSeveritySerializer(severity)
            result = severity_serializer.data
        return result

    def get_status_name(self,issue):
        result = dict()
        status = ProjectIssueStatus.objects.get_byvalue(issue.Status)
        if status:
            status_serializer = ProjectIssueStatuserializer(status)
            result = status_serializer.data
        return result

    def get_solution_name(self,issue):
        result = dict()
        resolved_result = ProjectIssueResolvedResult.objects.get_byvalue(issue.Solution)
        if resolved_result:
            resolved_serializer = ProjectIssueResolvedResultSerializer(resolved_result)
            result = resolved_serializer.data
        return result

    def get_category_name(self,issue):
        return ProjectIssueCategory.objects.get_byvalue(issue.IssueCategory).Name

    def get_priority_name(self,issue):
        return ProjectIssuePriority.objects.get_byvalue(issue.Priority).Name

    def get_project_phrase_name(self,issue):
        return ProjectPhase.objects.get_byvalue(issue.ProjectPhase).Name

    def creator_avatar(self,issue):
        result = "/static/global/images/fruit-avatar/Fruit-1.png"
        try:
            creator = User.objects.get(id=issue.Creator)
            if creator.extend_info:
                result = AccountService.get_avatar_url(creator)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_creator_name(self,issue):
        creator = User.objects.get(id=issue.Creator)
        result = creator.username
        if creator.first_name and creator.last_name:
            result = creator.last_name + creator.first_name
        return result

    def get_processor_name(self,issue):
        processor = User.objects.get(id=issue.Processor)
        result = processor.username
        if processor.first_name and processor.last_name:
            result = processor.last_name + processor.first_name
        return result

    def get_create_date(self,issue):
        result = "--"
        if issue.CreationTime:
            result = issue.CreationTime.astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
        return result

    def get_update_date(self,issue):
        result = "--"
        if issue.UpdateTime:
            result = DateTimeHelper.how_long_ago((datetime.datetime.now().replace(
                tzinfo=pytz.timezone(TIME_ZONE)) - issue.UpdateTime).seconds)
        return result

    def get_attachments_detail(self,issue):
        result = list()
        if issue.Attachments:
            for file_id in eval(issue.Attachments):
                file = FileInfo.objects.get(int(file_id))
                if file.IsActive != 0:
                    file_serializer = FileSerializer(file)
                    result.append(file_serializer.data)
        return result


    class Meta:

        model = ProjectIssue
        exclude = ('IsActive','CreationTime')
        extra_kwargs = {'Creator': {'required': False}, 'Solver': {'required': False},'Status': {'required': False},'Solution': {'required': False},'Project': {'required': False},'Version': {'required': False}}
        read_only_fields = ('id',)


class ProjectIssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueCategory
        exclude = ('IsActive',)
        read_only_fields = ('id',)

class ProjectOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOS
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectIssueStatuserializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueStatus
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectIssueResolvedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueResolvedResult
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectIssueSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueSeverity
        exclude = ('IsActive',)
        read_only_fields = ('id',)

class ProjectPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        exclude = ('IsActive',)
        read_only_fields = ('id',)

class ProjectIssuePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssuePriority
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModule
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectTaskSerializer(serializers.ModelSerializer):
    OwnerName = serializers.SerializerMethodField(method_name='get_owner_name')
    DeadLineFormat = serializers.SerializerMethodField(method_name='deadline_format')
    StartDateFormat = serializers.SerializerMethodField(method_name='startdate_format')
    PriorityFormator = serializers.SerializerMethodField(method_name='priority_formator')
    ChildStatus = serializers.SerializerMethodField(method_name='child_status')

    class Meta:
        model = models.Task
        fields = '__all__'
        read_only_fields = ('id', 'IsActive', 'OwnerName', 'ShowDeadLine', 'PriorityFormator')
        validators = []
        depth = 1

    def to_internal_value(self, data):
        return data

    def create(self, validated_data, user):
        task = TaskService.create_task(validated_data, user)
        return task

    def save(self, **kwargs):
        user = kwargs.get('user')
        self.is_valid()
        task = self.create(self.validated_data, user)
        return task

    def get_owner_name(self, obj):
        user_id =obj.Owner
        user = UserService.get_user(int(user_id))
        result = user.email[:1]
        user_name = user.last_name + user.first_name
        if len(user_name) >= 3:
            result = user_name[1:]
        else:
            result = user_name
        return result

    def priority_formator(self, obj):
        result = "#f5f7f9"

        if str(obj.Priority) == '1':
            result = "red"

        if str(obj.Priority) == '2':
            result = "blue"
        return result

    def child_status(self,obj):
        child_tasks = models.Task.objects.get_child_tasks(obj.id)
        child_finish_tasks = models.Task.objects.get_child_tasks(obj.id,1)
        result = ""
        if len(child_tasks)>0:
            result = str(len(child_finish_tasks))+"/"+str(len(child_tasks))
        return result


    def startdate_format(self,obj):
        result = obj.CreationTime

        if obj.StartDate and obj.StartDate != "":
            result = obj.StartDate

        return result

    def deadline_format(self, obj):
        '''
        :param obj:
        :return: 30天前
        remain_days<-30，return 30天前
        remain_days>-30，return 具体天数
        '''

        result = {"label":"","color":""}
        if obj.Status != 2 and obj.Status != 3:
            task = models.Task.objects.get(int(obj.id))
            remain_days = (task.DeadLine-datetime.date.today()).days
            if remain_days<-100:
                label = '3个月前'
                result = {"label":label,"color":"red"}

            if remain_days < 0 and remain_days>-100:
                label = str(abs(remain_days)) + '天前'
                result = {"label":label,"color":"error"}
            if remain_days > 0 and remain_days<=7:
                label = str(remain_days) + '天后'
                result = {"label":label,"color":"volcano"}
            if remain_days>7:
                label = str(remain_days) + '天后'
                result = {"label":label,"color":"default"}

            if remain_days == 0:
                result = {"label":"今天","color":"primary"}
        return result


class ProjectTaskVMSerializer(ProjectTaskSerializer):
    Child = ProjectTaskSerializer(many=True)

    class Meta:
        model = ApiProjectTask
        exclude = ('IsActive',)
        read_only_fields = ('id', 'Child')
        depth = 1

    def save(self, **kwargs):
        user = kwargs.get('user')
        self.update(self.instance, self.validated_data, user)

    def update(self, instance, validated_data, user):
        instance = TaskService.edit_task(instance, validated_data, user)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('IsActive', 'CreationTime', 'LabelColor')
        read_only_fields = ('id',)


class ProjectForTestingSerializer(serializers.ModelSerializer):
    OwnerName = serializers.SerializerMethodField(method_name='get_owner_name')
    DeadLineFormat = serializers.SerializerMethodField(method_name='deadline')
    Attachments = serializers.SerializerMethodField()
    VersionName = serializers.SerializerMethodField()
    ProjectName = serializers.SerializerMethodField()
    FortestingFeature = serializers.SerializerMethodField()


    class Meta:
        model = models.TestApplication
        fields = '__all__'
        validators = []
        read_only_fields = ('id', 'IsActive')
        extra_kwargs = {'Status': {'required': False}}


    def get_VersionName(self,obj):
        result = '--'
        if obj.VersionID:
            result = Version.objects.get(obj.VersionID).VVersion
        return result

    def get_FortestingFeature(self,obj):
        result3 = obj.TestingFeature.replace("<p>","").replace("</p>","").split("{;}")
        pattern1 = re.compile(r'<p>(.*?)</p>')
        result1 = pattern1.findall(obj.TestingFeature)
        return result1+result3


    def get_ProjectName(self,obj):
        result = '--'
        if obj.ProjectID:
            result = Project.objects.get(obj.ProjectID).PBTitle
        return result

    def get_Attachments(self,obj):
        result = list()
        if obj.Attachment:
            for file_id in eval(obj.Attachment):
                temp = dict()
                file = FileInfo.objects.get(int(file_id))
                if file:
                    temp['id'] = file_id
                    temp['name'] = file.FileName
                    temp['url'] = WEB_HOST+'/project/fortesting/download/'+str(file_id)
                    result.append(temp)
        return result





    def get_owner_name(self, obj):
        if obj.Commitor:
            owner_id = obj.Commitor
        else:
            owner_id = obj.Creator
        user = UserService.get_user(int(owner_id))
        result = user.email[:1]
        user_name = user.last_name + user.first_name
        if len(user_name) >= 3:
            result = user_name[1:]
        else:
            result = user_name
        return result

    def deadline(self, obj):
        '''
        :param obj:
        :return: 30天前
        remain_days<-30，return 30天前
        remain_days>-30，return 具体天数
        '''

        result = ''
        if obj.Status == 2 or obj.Status == 3:
            if obj.CommitTime:
                remain_days = (obj.CommitTime.replace(tzinfo=None) - datetime.datetime.today()).days
                if remain_days < -30:
                    result = '30天前'
                if remain_days > -30 and remain_days < 0:
                    result = str(abs(remain_days)) + '天前'
                if remain_days >= 0:
                    result = ''
        return result
