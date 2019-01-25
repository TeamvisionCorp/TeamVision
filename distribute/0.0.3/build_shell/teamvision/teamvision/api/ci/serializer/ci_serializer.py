# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci.models import CIDeployService, CaseTag
from teamvision.ci.models import CIServer, CICredentials, CITask
from teamvision.ci.models import CITaskHistory, CITaskPlugin
from business.auth_user.user_service import UserService
from business.project.version_service import VersionService
from business.ci.ci_task_parameter_service import CITaskParameterService
from teamvision.home.models import FileInfo
from teamvision.settings import WEB_HOST
from teamvision.project.models import Project
from gatesidelib.datetimehelper import DateTimeHelper
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from teamvision.ci.mongo_models import DeployServiceReplaceConfig, ReplaceFileMap, CITaskParameterGroup
import datetime,uuid


class CIDeployServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIDeployService
        exclude = ('CreateTime', 'IsActive')
        read_only_fields = ('id',)


class CIDeployServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIServer
        exclude = ('CreateTime', 'IsActive', 'Scope', 'Creator')
        read_only_fields = ('id',)


class CICaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTag
        exclude = ('CreateTime', 'IsActive')
        read_only_fields = ('id',)


class CITaskSerializer(serializers.ModelSerializer):
    ParameterGroups = serializers.SerializerMethodField()
    LastScheduleRunTime = serializers.DateTimeField(source='LastRunTime', required=False)
    LastRunTime = serializers.SerializerMethodField()
    LastRunStatus = serializers.SerializerMethodField()
    TaskConfigURI = serializers.SerializerMethodField()
    TaskHistoryURI = serializers.SerializerMethodField()
    ProjectName = serializers.SerializerMethodField()
    Display = serializers.SerializerMethodField()
    CopyTaskID = serializers.SerializerMethodField()
    UUID = serializers.SerializerMethodField()

    def get_ParameterGroups(self, obj):
        parameter_groups = CITaskParameterService.task_parameter_list(obj.id)
        result = list()
        for item in parameter_groups:
            temp = dict()
            temp['id'] = str(item.id)
            temp['title'] = item.group_name
            temp['default'] = item.is_default
            result.append(temp)
        return result

    def get_Display(self, obj):
        return True

    def get_CopyTaskID(self, obj):
        return 0

    def get_UUID(self,obj):
        return uuid.uuid1()

    def get_LastRunTime(self, obj):
        result = '--'
        history = None
        try:
            history = CITaskHistory.objects.filter(CITaskID=obj.id).latest('StartTime')
        except Exception as ex:
            pass
        if history:
            if history.StartTime:
                str_start_time = str(history.StartTime + datetime.timedelta(hours=8))[:19]
                result = str_start_time
        return result

    def get_LastRunStatus(self, obj):
        result = 0
        history = None
        try:
            history = CITaskHistory.objects.filter(CITaskID=obj.id).latest('StartTime')
        except Exception as ex:
            pass
        if history:
            result = history.BuildStatus
        return result

    def get_TaskConfigURI(self, obj):
        task_type_name = self.task_type_name(obj)
        return WEB_HOST + '/ci/' + task_type_name + '/' + str(obj.id) + '/config'

    def get_TaskHistoryURI(self, obj):
        task_type_name = self.task_type_name(obj)
        return WEB_HOST + '/ci/' + task_type_name + '/' + str(obj.id) + '/history'

    def get_ProjectName(self, obj):
        return Project.objects.get(obj.Project).PBTitle

    def task_type_name(self, ci_task):
        result = "build"
        if ci_task.TaskType == 4:
            result = "build"

        if ci_task.TaskType == 5:
            result = "deploy"

        if ci_task.TaskType == 1:
            result = "testing"
        return result

    class Meta:
        model = CITask
        exclude = ('IsActive',)
        read_only_fields = ('id',)
        extra_kwargs = {'LastRunTime': {'required': False}}


class CIDeployServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIServer
        exclude = ('CreateTime', 'IsActive', 'Scope', 'Creator')
        read_only_fields = ('id',)


class CITaskPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CITaskPlugin
        exclude = ('CreateTime', 'IsActive')
        read_only_fields = ('id',)


class CICrendentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CICredentials
        exclude = ('CreateTime', 'IsActive')
        read_only_fields = ('id', 'ProjectName')


class CITaskOperationSerializer(serializers.Serializer):
    tq_id = serializers.IntegerField()
    message = serializers.CharField()


class CITaskHistorySerializer(serializers.ModelSerializer):
    StartTimeFormat = serializers.SerializerMethodField()
    StartTimeFormatString = serializers.SerializerMethodField()
    EndTimeFormat = serializers.SerializerMethodField()
    StartedUser = serializers.SerializerMethodField()
    ProjectVersionFormat = serializers.SerializerMethodField()
    Package = serializers.SerializerMethodField()
    BuildLog = serializers.SerializerMethodField()
    TaskName = serializers.SerializerMethodField()
    TaskHistoryURI = serializers.SerializerMethodField()

    class Meta:
        model = CITaskHistory
        exclude = ('CreateTime', 'PackageID', 'BuildLogID')
        extra_kwargs = {'BuildMessage': {'required': False},'FlowSectionHistory': {'required': False}}
        read_only_fields = ('id','IsActive')

    def get_Package(self, obj):
        result = ""
        if obj.PackageID:
            for file_id in eval(obj.PackageID):
                file_info = FileInfo.objects.get(file_id)
                result = result + file_info.FileName + "{|}" + WEB_HOST + "/ci/history/" + str(
                    file_id) + "/download_package{|}" + str(file_id) + ","
        return result

    def get_BuildLog(self, obj):
        result = ""
        if obj.BuildLogID:
            file_info = FileInfo.objects.get(obj.BuildLogID)
            result = WEB_HOST + "/ci/history/buildlog/" + str(obj.BuildLogID)
        return result

    def get_StartTimeFormat(self, obj):
        result = 0
        if obj.StartTime:
            result = obj.StartTime.timestamp() * 1000
        return str(result)

    def get_StartTimeFormatString(self, obj):
        result = 0
        if obj.StartTime:
            result = str(obj.StartTime)[:19]
        return str(result)

    def get_TaskHistoryURI(self, obj):
        task = CITask.objects.get(obj.CITaskID)
        if task:
            task_type_name = self.task_type_name(task)
        return WEB_HOST + '/ci/' + task_type_name + '/' + str(obj.CITaskID) + '/history'

    def task_type_name(self, ci_task):
        result = "build"
        if ci_task.TaskType == 4:
            result = "build"

        if ci_task.TaskType == 5:
            result = "deploy"

        if ci_task.TaskType == 1:
            result = "testing"
        return result

    def get_EndTimeFormat(self, obj):
        result = 0
        if obj.EndTime:
            result = obj.EndTime.timestamp() * 1000
        return str(result)

    def get_StartedUser(self, obj):
        result = '系统定时任务触发'
        user = UserService.get_user(obj.StartedBy)
        if user:
            result = user.last_name + user.first_name
        return result

    def get_TaskName(self,obj):
        result = '--'
        task = CITask.objects.get(obj.CITaskID)
        if task:
            result = task.TaskName
        return result

    def get_ProjectVersionFormat(self, obj):
        result = '--'
        version = VersionService.get_version(obj.ProjectVersion)
        if version:
            result = version.VVersion
        return result


class ServiceReplaceTargetSerializer(EmbeddedDocumentSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ReplaceFileMap
        fields = '__all__'

    def get_file_url(self, obj):
        return WEB_HOST + "/ci/service/download_file/" + str(obj.file_id)


class ServiceReplaceConfigSerializer(DocumentSerializer):
    replace_target_map = ServiceReplaceTargetSerializer(many=True)

    class Meta:
        model = DeployServiceReplaceConfig
        fields = ('replace_target_map',)
        depth = 2


class TaskParameterGroupSerializer(DocumentSerializer):
    class Meta:
        model = CITaskParameterGroup
        fields = '__all__'
        read_only_fields = ('id', 'is_default')
        depth = 2


class CIProjectSerializer(serializers.ModelSerializer):
    ProjectName = serializers.CharField(source='PBTitle')
    CITasks = serializers.SerializerMethodField()
    CITaskCount = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ('CreationTime', 'IsActive')
        read_only_fields = ('id',)

    def get_CITasks(self, obj):
        result = list()
        ci_tasks = CITask.objects.project_tasks(obj.id)
        for task in ci_tasks:
            temp = dict()
            temp['TaskName'] = task.TaskName
            temp['TaskHistoryURL'] = self.get_TaskHistoryURI(task)
            temp['ID'] = task.id
            temp['Display'] = True
            result.append(temp)
        return result

    def get_CITaskCount(self, obj):
        return len(self.get_CITasks(obj))

    def get_TaskHistoryURI(self, obj):
        task_type_name = self.task_type_name(obj)
        return 'http://teamcat.qyvideo.net/ci/' + task_type_name + '/' + str(obj.id) + '/history'

    def task_type_name(self, ci_task):
        result = "build"
        if ci_task.TaskType == 4:
            result = "build"

        if ci_task.TaskType == 5:
            result = "deploy"

        if ci_task.TaskType == 1:
            result = "testing"
        return result
