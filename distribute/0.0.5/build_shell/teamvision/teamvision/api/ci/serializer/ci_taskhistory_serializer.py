#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci.models import CITask,AutoTestingTaskResult
from teamvision.ci.models import CITaskHistory,CITaskStageHistory,CITaskStepOutput
from teamvision.ci import mongo_models
from business.auth_user.user_service import UserService
from business.project.version_service import VersionService
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_config_service import CITaskConfigService
from teamvision.home.models import FileInfo,Agent
from teamvision.settings import WEB_HOST



class CITaskHistorySerializer(serializers.ModelSerializer):
    ViewFormat = serializers.SerializerMethodField()
    StageHistory = serializers.SerializerMethodField()


    class Meta:
        model = CITaskHistory
        exclude = ('CreateTime',)
        extra_kwargs = {'FlowSectionHistory': {'required': False}}
        read_only_fields = ('id','IsActive')

    def get_StartTimeFormat(self, obj):
        result = 0
        if obj.StartTime:
            result = str(obj.StartTime)[:19]
        return str(result)

    def get_CurrenStageIndex(self,obj):
        result = -1
        stage_history_list = CITaskStageHistory.objects.filter(TaskHistoryID=obj.id).order_by('id')
        index = 1
        for history in stage_history_list:
            if history.Status == 1:
                result = index
            index = index + 1
        return result

    def get_ViewFormat(self,obj):
        result = dict()
        result['StartTime'] = self.get_StartTimeFormat(obj)
        result['EndTimestamp'] = self.get_EndTimeFormat(obj)
        result['StartTimestamp'] = self.get_StartTimeStampFormat(obj)
        result['ProjectVersion'] = self.get_ProjectVersionFormat(obj)
        result['TaskName'] = self.get_TaskName(obj)
        result['AgentName'] = self.get_AgentName(obj)
        result['StartBy'] = self.get_StartedUser(obj)
        result['TaskType'] = self.task_type_name(obj)
        result['Duration'] = self.get_Duration(obj)
        result['CurrentStageIndex'] = self.get_CurrenStageIndex(obj)
        result['TaskHistoryURI'] = self.get_TaskHistoryURI(obj)
        return result

    def get_TaskHistoryURI(self, obj):
        return WEB_HOST + '/ci/task/' + str(obj.CITaskID) + '/history'

    def task_type_name(self, obj):
        result = "构建"
        ci_task = CITask.objects.get(obj.CITaskID)
        if ci_task.TaskType == 4:
            result = "构建"

        if ci_task.TaskType == 5:
            result = "部署"

        if ci_task.TaskType == 1:
            result = "测试"
        return result

    def get_EndTimeFormat(self, obj):
        result = 0
        if obj.EndTime:
            result = obj.EndTime.timestamp() * 1000
        return str(result)

    def get_StartTimeStampFormat(self, obj):
        result = 0
        if obj.StartTime:
            result = obj.StartTime.timestamp() * 1000
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

    def get_AgentName(self,obj):
        result = "--"
        if obj.AgentID is not None:
            agent = Agent.objects.get(obj.AgentID)
            if agent is not None:
                result = agent.Name
        return result

    def get_Duration(self,obj):
        result="--"
        if obj.StartTime and obj.EndTime:
            durations=(obj.EndTime-obj.StartTime).total_seconds()
            result=int(durations/60)
            if result==0:
                result=str(durations)+"秒"
            else:
                result=str(result)+"分钟"
        return result

    def get_StageHistory(self,obj):
        stage_history_list = CITaskStageHistory.objects.filter(TaskHistoryID=obj.id).order_by('id')
        serializer = CITaskStageHistorySerializer(stage_history_list, many=True)
        return serializer.data


class CITaskStageHistorySerializer(serializers.ModelSerializer):
    ViewFormat = serializers.SerializerMethodField()

    def get_StageOutputPackage(self,obj):
        stage_output_list = CITaskStepOutput.objects.filter(StageHistoryID=obj.id).filter(ProductType__in=(2,3,6)).order_by('id')
        serializer = CITaskOutputSerializer(stage_output_list, many=True)
        return serializer.data

    def get_StageOutputLog(self,obj):
        stage_output_list = CITaskStepOutput.objects.filter(StageHistoryID=obj.id).filter(ProductType=1).order_by('id')
        serializer = CITaskOutputSerializer(stage_output_list, many=True)
        return serializer.data

    def get_StageOutputCodeVersion(self,obj):
        stage_output_list = CITaskStepOutput.objects.filter(StageHistoryID=obj.id).filter(ProductType=5).order_by('id')
        serializer = CITaskOutputSerializer(stage_output_list, many=True)
        return serializer.data

    def get_StageOutputChangeLog(self,obj):
        stage_output_list = CITaskStepOutput.objects.filter(StageHistoryID=obj.id).filter(ProductType=4).order_by('id')
        serializer = CITaskOutputSerializer(stage_output_list, many=True)
        return serializer.data


    def get_StageName(self,obj):
        result = ""
        stage = CITaskConfigService.task_stage(obj.StageID)
        if stage is not None:
            result = stage.stage_title
        return result

    def get_StatusName(self,obj):
        result = 'wait'
        if obj.Status == 0:
            result = 'wait'

        if obj.Status == 1:
            result = 'process'

        if obj.Status == 2:
            result = 'finish'

        if obj.Status == 3:
            result = 'error'

        if obj.Status == 4:
            result = 'error'
        return result

    def get_Duration(self,obj):
        result="--"
        if obj.StartTime and obj.EndTime:
            durations=(obj.EndTime-obj.StartTime).total_seconds()
            result=int(durations/60)
            if result==0:
                result=str(durations)+"秒"
            else:
                result=str(result)+"分钟"
        return result

    def get_NextStageHisory(self,obj):
        result = None
        stage_histories = CITaskStageHistory.objects.get_sthistory_bythistory_id(obj.TaskHistoryID).order_by('id')
        index = 0
        for history in stage_histories:
            if history.id == obj.id:
                if len(stage_histories) ==1:
                    break
                if index < len(stage_histories)-1:
                    result = stage_histories[index+1].id
                break
            index = index+1
        return result

    def get_PreviousStageHisory(self,obj):
        result = None
        stage_histories = CITaskStageHistory.objects.get_sthistory_bythistory_id(obj.TaskHistoryID).order_by('id')
        index = 0
        for history in stage_histories:
            if history.id == obj.id:
                if len(stage_histories) ==1:
                    break
                if index >= 1:
                    result = stage_histories[index -1].id
                break
            index = index + 1
        return result

    def get_BuildVersion(self,obj):
        result = ""
        task_history = CITaskHistory.objects.get(obj.TaskHistoryID)
        if task_history:
            result = task_history.BuildVersion
        return result




    def get_TestResults(self,obj):
        result = list()
        test_results = AutoTestingTaskResult.objects.get_by_historyid(obj.id)
        for test_result in test_results:
            temp = dict()
            temp['result_id'] = test_result.id
            temp['total'] = test_result.Total
            temp['pass'] = test_result.Pass
            temp['fail'] = test_result.Fail
            temp['aborted'] = test_result.Aborted
            temp['purpose_name'] = self.get_step_name(test_result.StepID)
            temp['step_id'] = test_result.StepID
            result.append(temp)
        return result

    def get_step_name(self,step_id):
        result = ''
        task_step = CITaskConfigService.task_step(step_id)
        if task_step and task_step.purpose_name.strip():
            result = task_step.purpose_name
        return result


    def get_ViewFormat(self,obj):
        result = dict()
        result['StageOutputPackage'] = self.get_StageOutputPackage(obj)
        result['StageOutputLog'] = self.get_StageOutputLog(obj)
        result['StageOutputCodeVersion'] = self.get_StageOutputCodeVersion(obj)
        result['StageOutputChangeLog'] = self.get_StageOutputChangeLog(obj)
        result['StageName'] = self.get_StageName(obj)
        result['Status'] = self.get_StatusName(obj)
        result['TestResults'] = self.get_TestResults(obj)
        result['Show'] = False
        result['TagLeft'] = '0px'
        result['NextStageHistory'] = self.get_NextStageHisory(obj)
        result['PreviousStageHisory'] = self.get_PreviousStageHisory(obj)
        result['Duration'] = self.get_Duration(obj)
        result['BuildVersion'] = self.get_BuildVersion(obj)
        return result




    class Meta:
        model = CITaskStageHistory
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)


class CITaskOutputSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    step_name = serializers.SerializerMethodField()
    commit_info = serializers.SerializerMethodField()

    def get_product_name(self,obj):
        result = None
        if obj.ProductType ==3 or obj.ProductType ==2 or obj.ProductType==6:
            if obj.ProductID:
                file = FileInfo.objects.get(obj.ProductID)
                if file:
                    result = file.FileName
        return result

    def get_step_name(self,obj):
        result = "--"
        task_step = CITaskConfigService.task_step(obj.StepID)
        if task_step:
            result = str(task_step.step_config["step_name"])+" "+str(task_step.purpose_name)
        return result

    def get_commit_info(self,obj):
        result = list()
        if obj.CodeVersion:
            for version in eval(obj.CodeVersion):
                temp_info = dict()
                temp_info["code_repo"] = version["repo"]
                temp_info["version"] = version["version"]
                result.append(temp_info)
        return result



    class Meta:
        model = CITaskStepOutput
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)