# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.auth_extend.user.models import ActionLog
from business.auth_user.user_service import UserService
import datetime
from gatesidelib.datetimehelper import DateTimeHelper


class ToDoSummarySerializer(serializers.Serializer):
    task_count = serializers.IntegerField()
    issue_count = serializers.IntegerField()
    fortesting_count = serializers.IntegerField()

    class Meta:
        read_only_fields = ('task_count', 'issue_count', 'fortesting_count')

    def save(self):
        raise Exception("only get request")

class LogActionSerializer(serializers.ModelSerializer):
    UserName = serializers.SerializerMethodField()
    ActionTimeStr = serializers.SerializerMethodField()

    class Meta:
        model = ActionLog
        fields = '__all__'
        # read_only_fields = ('task_count', 'issue_count', 'fortesting_count')


    def get_UserName(self,obj):
        user = UserService.get_user(obj.User)
        result = '系统'
        if user:
            user_name = user.last_name + user.first_name
            if len(user_name) >= 3:
                result = user_name[1:]
            else:
                result = user_name
        return result

    def get_ActionTimeStr(self,obj):
        now= datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        action_time=datetime.datetime.strptime(obj.ActionTime.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        action_time=action_time + datetime.timedelta(hours=8)
        time_internal=(now-action_time).total_seconds()
        return DateTimeHelper.how_long_ago(time_internal)

    def save(self):
        raise Exception("only get request")


