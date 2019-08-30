#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.project import mongo_models
from rest_framework_mongoengine.serializers import DocumentSerializer,EmbeddedDocumentSerializer


extra_kwargs = {'BugTrendAttachments': {'required': False},'CCList': {'required': False},'Commnents': {'required': False}}

class BVTReportSerializer(DocumentSerializer):
    class Meta:
        model=mongo_models.BVTReport
        exclude=('is_active','create_time')
        read_only_fields=('id',)
        depth=2

class TestProgressReportSerializer(DocumentSerializer):
    class Meta:
        model=mongo_models.TestProgressReport
        exclude=('is_active','create_time')
        extra_kwargs = extra_kwargs
        read_only_fields=('id',)
        depth=2

class TestingCompleteReportSerializer(DocumentSerializer):
    class Meta:
        model=mongo_models.TestingCompleteReport
        exclude=('is_active','create_time','ProjectInfo')
        extra_kwargs = extra_kwargs
        read_only_fields=('id',)
        depth=2



        
        
        