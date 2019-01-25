# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from doraemon.project.models import ProjectModule, ProjectIssueStatus, Version, ProjectModule, ProjectIssue, \
    ProjectIssueCategory, ProjectIssueResolvedResult, ProjectIssueSeverity, Product,Project
from doraemon.project import models
from doraemon.settings import WEB_HOST
from doraemon.home.models import FileInfo
from doraemon.api.project.viewmodel.api_project_task import ApiProjectTask
from doraemon.api.project.viewmodel.api_project_member import ApiProjectMember
from doraemon.api.project.viewmodel.api_project import ApiProject
from gatesidelib.datetimehelper import DateTimeHelper
from business.auth_user.user_service import UserService
from business.project.task_service import TaskService
import datetime,re


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
    class Meta:
        model = ProjectIssue
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectIssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueCategory
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


class ProjectModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModule
        exclude = ('IsActive',)
        read_only_fields = ('id',)


class ProjectTaskSerializer(serializers.ModelSerializer):
    OwnerName = serializers.SerializerMethodField(method_name='get_owner_name')
    DeadLineFormat = serializers.SerializerMethodField(method_name='deadline')
    PriorityFormator = serializers.SerializerMethodField(method_name='priority_formator')

    class Meta:
        model = models.Task
        exclude = ('Parent',)
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
        user_id = eval(obj.Owner)[0]
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
            result = "#8c0776"

        if str(obj.Priority) == '2':
            result = "blue"
        return result

    def deadline(self, obj):
        '''
        :param obj:
        :return: 30天前
        remain_days<-30，return 30天前
        remain_days>-30，return 具体天数
        '''

        result = ''
        if obj.Status != 1 and obj.Status != 3:
            remain_days = (obj.DeadLine-datetime.date.today()).days
            if remain_days < -30:
                result = '30天前'
            if remain_days > -30 and remain_days < 0:
                result = str(abs(remain_days)) + '天前'
            if remain_days >= 0:
                result = ''
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
        pattern1 = re.compile(r'<p>(.*?)</p>')
        pattern2 = re.compile(r'<li>(.*?)</li>')
        result1 = pattern1.findall(obj.TestingFeature)
        result2 = pattern2.findall(obj.TestingFeature)
        return result1+result2


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
