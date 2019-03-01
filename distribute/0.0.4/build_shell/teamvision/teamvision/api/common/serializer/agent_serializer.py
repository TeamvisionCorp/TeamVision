#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import Agent,TaskQueue
from teamvision.ci.models import CITask
from business.ci.ci_task_queue_service import CITQService
import datetime
from gatesidelib.datetimehelper import DateTimeHelper

class AgentSerializer(serializers.ModelSerializer):
    RunningTasks = serializers.SerializerMethodField()

    def get_RunningTasks(self,obj):
        tasks = list()
        queues = TaskQueue.objects.get_agent_tasks(obj.id)
        for queue in queues:
            if queue.TaskType not in(6,7):
                task = CITask.objects.get(queue.TaskID)
                if task:
                    temp=dict()
                    temp['TQID'] = queue.id
                    temp['TaskUUID'] = queue.TaskUUID
                    temp['TaskID'] = task.id
                    temp['TaskName'] = task.TaskName
                    temp['TriggerName'] = CITQService.start_user(queue.id)
                    temp['Process'] = self.get_build_process(queue)
                    tasks.append(temp)
        return tasks

    def get_build_process(self,ci_task_queue):
        result=20
        if ci_task_queue:
            if ci_task_queue.StartTime:
                start_time=ci_task_queue.StartTime+datetime.timedelta(hours=8)
                duration=DateTimeHelper.get_time_to_now(str(start_time)[:19],"%Y-%m-%d %H:%M:%S")
                result=int(duration)/10
                if result>90:
                    result=90
                elif result<0:
                    result=5
            else:
                result=5
        return result

    class Meta:
        model = Agent
        exclude=('IsActive','CreationTime')
        read_only_fields = ('id',)
        
        
        