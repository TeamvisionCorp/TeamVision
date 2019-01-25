#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci.models import CITaskFlow,CITaskHistory,CITaskFlowHistory,CITaskFlowSection,CITask,CIFlowSectionHistory
from teamvision.api.ci.viewmodel.api_ci_taskflow import ApiCITaskFlow
from teamvision.api.ci.serializer.ci_serializer import CITaskSerializer
from teamvision.api.ci.serializer import ci_serializer
from business.auth_user.user_service import UserService
from gatesidelib.datetimehelper import DateTimeHelper
import datetime


class CITaskFlowSectionSerializer(serializers.ModelSerializer):
    Tasks = serializers.SerializerMethodField()
    CITaskIDs = serializers.SerializerMethodField()
    SectionIndex = serializers.SerializerMethodField()


    def get_Tasks(self,obj):
        result = list()
        for task_id in self.get_CITaskIDs(obj):
            temp = CITask.objects.get(task_id)
            if temp:
                task_serializer = CITaskSerializer(instance=temp)
                result.append(task_serializer.data)
        return result


    def get_CITaskIDs(self,obj):
        result = list()
        task_ids = obj.CITasks.lstrip(',')
        if ',' in task_ids or '[' in task_ids:
            for task_id in eval(obj.CITasks.lstrip(',')):
                result.append(task_id)
        else:
            if task_ids.strip(',')!='':
                result.append(int(task_ids.strip(',')))
        return result


    def get_SectionIndex(self,obj):
        result = 0
        flowSections = CITaskFlowSection.objects.flow_sections(obj.TaskFlow)
        index =0
        for section in flowSections:
            if obj.id == section.id:
                result = index+1
                break;
            index= index+1
        return result


    class Meta:
        model = CITaskFlowSection
        exclude = ('IsActive','CreateTime')
        extra_kwargs = {'CITasks': {'required': False}}
        read_only_fields = ('id',)
        write_only_fields = ('CITasks',)


class CITaskFlowListSerializer(serializers.ModelSerializer):
    LastRunTime = serializers.SerializerMethodField(method_name='get_last_runtime')

    def get_last_runtime(self,obj):
        if obj.LastRunTime:
            return str((obj.LastRunTime+datetime.timedelta(hours=8)))[:19]
        else:
            return obj.LastRunTime


    class Meta:
        model = CITaskFlow
        exclude = ('IsActive',)
        read_only_fields = ('id',)
        extra_kwargs = {'LastRunTime': {'required': False},'Description': {'required': False}}


class CITaskFlowSerializer(serializers.ModelSerializer):
    Sections = CITaskFlowSectionSerializer(many=True)
    MaxOrder = serializers.SerializerMethodField()


    def get_MaxOrder(self,obj):
        result = 1
        flowSections = CITaskFlowSection.objects.flow_sections(obj.id).order_by('-SectionOrder')
        if len(flowSections)>0:
            result = flowSections[0].SectionOrder
        return result

    class Meta:
        model = ApiCITaskFlow
        exclude = ('IsActive',)
        read_only_fields = ('id',)
        extra_kwargs = {'LastRunTime': {'required': False},'Description': {'required': False}}


class CITaskFlowHistorySerializer(serializers.ModelSerializer):
    SectionHistories = serializers.SerializerMethodField()
    StartTimeFormat = serializers.SerializerMethodField()
    StartedUser = serializers.SerializerMethodField()


    def get_SectionHistories(self,obj):
        result =list()
        flow_section_histories = CIFlowSectionHistory.objects.flow__section_history(obj.id)
        for section_history in flow_section_histories:
            section_history_serializer = CIFlowSectionHistorySerializer(instance=section_history)
            result.append(section_history_serializer.data)
        return result

    def get_StartedUser(self, obj):
        result = '系统'
        user = UserService.get_user(obj.StartedBy)
        if user:
            result = user.last_name + user.first_name
            result=result[-2:]
        return result


    def get_StartTimeFormat(self,obj):
        result = '--'
        if obj.StartTime:
            result = str(obj.StartTime)[:19]
        return result


    class Meta:
        model = CITaskFlowHistory
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)

class CIFlowSectionHistorySerializer(serializers.ModelSerializer):
    TaskHistories = serializers.SerializerMethodField()
    SectionName = serializers.SerializerMethodField()
    SectionIndex = serializers.SerializerMethodField()

    def get_TaskHistories(self,obj):
        result = list()
        task_histories = CITaskHistory.objects.get_history_by_sechistory(obj.id,is_active=0)
        for task_history in task_histories:
            task_history_serializer = ci_serializer.CITaskHistorySerializer(instance=task_history)
            result.append(task_history_serializer.data)
        return result

    def get_SectionName(self,obj):
        result = '默认'
        section = CITaskFlowSection.objects.get(obj.Section)
        if section:
            result = section.SectionName
        return result


    def get_SectionIndex(self,obj):
        result = 0
        flowSections = CITaskFlowSection.objects.flow_sections(obj.TaskFlow)
        index =0
        for section in flowSections:
            if obj.Section == section.id:
                result = index+1
                break;
            index= index+1
        return result


    class Meta:
        model = CIFlowSectionHistory
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)

           

