#coding=utf-8
'''
Created on 2016-10-12

@author: Administrator
'''

from rest_framework import serializers
from teamvision.logcat.models import Logger
from teamvision.logcat.mongo_models import BusinessLog
from rest_framework_mongoengine.serializers import DocumentSerializer

class LoggerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Logger
        exclude=('CreationTime','IsActive',)
        read_only_fields = ('id',)


class BusinessLogSerializer(DocumentSerializer):
    class Meta:
        model=BusinessLog
        exclude=('is_active','create_time')
#         fields = ('id','appId','eventId','userId','channel','model','os','data','device_id','app_version','build_version')
        read_only_fields=('id',)
        depth=2
        
        
        