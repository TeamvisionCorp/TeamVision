#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import Agent,TaskQueue
from teamvision.project.models import TagOwner,Tag
from teamvision.ci.models import CITask
from business.ci.ci_task_queue_service import CITQService
from teamvision.api.project.serializer.project_serializer import  ProjectTagSerializer
import datetime
from gatesidelib.datetimehelper import DateTimeHelper

class AgentSerializer(serializers.ModelSerializer):
    RunningTasks = serializers.SerializerMethodField()
    AgentTags = serializers.SerializerMethodField()
    TagFormat = serializers.SerializerMethodField()

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

    def get_TagFormat(self,obj):
        result = []
        tag_owner = TagOwner.objects.get_tags(obj.id,3)
        tag_ids = [tag.TagID for tag in tag_owner]
        for tag_id in tag_ids:
            temp_tag = Tag.objects.get(int(tag_id))
            serializer = ProjectTagSerializer(instance=temp_tag)
            result.append(serializer.data)
        return  result


    def get_AgentTags(self,obj):
        tag_owner = TagOwner.objects.get_tags(obj.id,3)
        result = [tag.TagID for tag in tag_owner]
        return  result



    class Meta:
        model = Agent
        exclude=('IsActive','CreationTime')
        extra_kwargs = {'IP': {'required': False},'OS': {'required': False}}
        read_only_fields = ('id',)
        
        
        