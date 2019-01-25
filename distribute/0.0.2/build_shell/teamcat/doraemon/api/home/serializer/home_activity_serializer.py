# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from doraemon.auth_extend.user.models import ActionLog


class LogActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionLog
        # read_only_fields = ('task_count', 'issue_count', 'fortesting_count')

    def save(self):
        raise Exception("only get request")


