#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import FileInfo
from teamvision.settings import TIME_ZONE
from teamvision.ci.models import CITask
from business.ci.ci_task_queue_service import CITQService
import datetime
from gatesidelib.datetimehelper import DateTimeHelper
import pytz

class FileSerializer(serializers.ModelSerializer):
    CreationTimeFormat = serializers.SerializerMethodField()



    def get_CreationTimeFormat(self,obj):
        result = '--'
        if obj.CreationTime:
            result = obj.CreationTime.astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
        return result

    class Meta:
        model = FileInfo
        exclude=('IsActive',)
        read_only_fields = ('id',)
        
        
        