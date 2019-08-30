# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci.models import CaseTag
from teamvision.ci.models import CICredentials, CITask,CITaskPlugin,CaseTag
from teamvision.ci.models import CITaskHistory, CITaskPlugin,CITaskApiTrigger
from teamvision.ci import mongo_models
from business.auth_user.user_service import UserService
from business.project.version_service import VersionService
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_config_service import CITaskConfigService
from teamvision.home.models import FileInfo
from teamvision.settings import WEB_HOST
from teamvision.project.models import Project
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from teamvision.api.ci.serializer.ci_step_serializer import CITaskStepSerializer
from teamvision.ci.mongo_models import  CITaskParameterGroup,CITaskStage,CITaskDefaultStage
import datetime,uuid




class CICaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTag
        exclude = ('CreateTime', 'IsActive')
        read_only_fields = ('id',)


class CITaskTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CITaskApiTrigger
        exclude = ('CreateTime',)
        read_only_fields = ('id',)



class CITaskPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CITaskPlugin
        exclude = ('CreateTime',)
        read_only_fields = ('id',)


class CITaskSerializer(serializers.ModelSerializer):
    ParameterGroups = serializers.SerializerMethodField()
    LastScheduleRunTime = serializers.DateTimeField(source='LastRunTime', required=False,allow_null=True)
    LastRunTime = serializers.SerializerMethodField()
    LastRunStatus = serializers.SerializerMethodField()
    TaskConfigURI = serializers.SerializerMethodField()
    TaskHistoryURI = serializers.SerializerMethodField()
    ProjectName = serializers.SerializerMethodField()
    Display = serializers.SerializerMethodField()
    CopyTaskID = serializers.SerializerMethodField()
    UUID = serializers.SerializerMethodField()
    AgentFilterType = serializers.SerializerMethodField()
    AgentTags = serializers.SerializerMethodField()
    AgentID = serializers.SerializerMethodField()

    def get_ParameterGroups(self, obj):
        parameter_groups = CITaskParameterService.task_parameter_list(obj.id)
        result = list()
        for item in parameter_groups:
            temp = dict()
            temp['id'] = str(item.id)
            temp['title'] = item.group_name
            temp['default'] = item.is_default
            temp['parameters'] = list()
            i = 1
            if item.parameters is not None:
                for parameter in item.parameters:
                    temp_dict = dict()
                    temp_dict['id'] = i
                    temp_dict['key'] = parameter.key
                    temp_dict['value'] = parameter.value
                    temp_dict['description'] = parameter.description
                    temp['parameters'].append(temp_dict)
                    i = i + 1
            result.append(temp)
        return result

    def get_Display(self, obj):
        return True

    def get_CopyTaskID(self, obj):
        return 0

    def get_AgentFilterType(self,obj):
        result = 1
        default_stage = CITaskConfigService.task_default_sage(obj.id)
        if default_stage:
            result = default_stage.agent_filter.filter_type
        return result

    def get_AgentTags(self,obj):
        result = list()
        default_stage = CITaskConfigService.task_default_sage(obj.id)
        if default_stage:
            result = default_stage.agent_filter.agent_tags
        return result

    def get_AgentID(self,obj):
        result = 0
        default_stage = CITaskConfigService.task_default_sage(obj.id)
        if default_stage:
            result = default_stage.agent_filter.agent_id
        return result

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
            result = history.Status
        return result

    def get_TaskConfigURI(self, obj):
        return WEB_HOST + '/ci/task/' + str(obj.id) + '/config'

    def get_TaskHistoryURI(self, obj):
        return WEB_HOST + '/ci/task/' + str(obj.id) + '/history'

    def get_ProjectName(self, obj):
        return Project.objects.get(obj.Project).PBTitle

    def task_type_name(self, ci_task):
        return "task"

    class Meta:
        model = CITask
        exclude = ('IsActive',)
        read_only_fields = ('id',)
        extra_kwargs = {'LastRunTime': {'required': False}}




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





class CITaskStageSerializer(EmbeddedDocumentSerializer):

    class Meta:
        model = mongo_models.ParameterStepSettings
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1


class TaskParameterGroupSerializer(DocumentSerializer):

    class Meta:
        model = CITaskParameterGroup
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1


class CITaskStageSerializer(DocumentSerializer):
    steps = serializers.SerializerMethodField()

    def get_steps(self,obj):
        queryset = mongo_models.CITaskStep.objects.all().filter(stage_id=str(obj.id)).order_by('step_order_index')
        serializer = CITaskStepSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = CITaskStage
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1


class CITaskDefaultStageSerializer(DocumentSerializer):

    class Meta:
        model = CITaskDefaultStage
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1


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
        return WEB_HOST+'/ci/task/' + str(obj.id) + '/history'

    def task_type_name(self, ci_task):
        return "task"
