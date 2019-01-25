#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import TaskQueue
from teamvision.ci.models import CITask
from business.ci.ci_task_queue_service import CITQService
from business.ci.ci_task_service import CITaskService
class TaskQueueSerializer(serializers.ModelSerializer):
    TriggerName = serializers.SerializerMethodField()
    TaskName = serializers.SerializerMethodField()

    def get_TriggerName(self,obj):
        return CITQService.start_user(obj.id)

    def get_TaskName(self,obj):
        result = '--'
        task = CITask.objects.get(obj.TaskID)
        if task:
            result = task.TaskName
        return result



    class Meta:
        model = TaskQueue
        read_only_fields = ('id',)
        fields='__all__'
        extra_kwargs = {'AgentID': {'required': False},'ParentID': {'required': False},'TaskType': {'required': False}, 'MobileDeviceID': {'required': False},'RerunReportID': {'required': False},'RuntimeEnv': {'required': False},'DistributeTimes': {'required': False}}
        
        
        