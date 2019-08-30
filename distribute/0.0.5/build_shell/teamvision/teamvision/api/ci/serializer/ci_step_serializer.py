#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci import mongo_models
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
import datetime


class CITaskSvnStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskSVNStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskSvnStepSerializer(instance=mongo_models.CITaskSVNStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data

    def step_id(self):
        return str(mongo_models.CITaskSVNStep().step_id)


class CITaskGitStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskSVNStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):
        serializer = CITaskGitStepSerializer(instance=mongo_models.CITaskGitStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data
    
    def step_id(self):
        return str(mongo_models.CITaskGitStep().step_id)

class CITaskIOSStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskIOSStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskIOSStepSerializer(instance=mongo_models.CITaskIOSStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data

    def step_id(self):
        return str(mongo_models.CITaskIOSStep().step_id)

class CITaskAndroidStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskAndroidStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskAndroidStepSerializer(instance=mongo_models.CITaskAndroidStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data
    def step_id(self):
        return str(mongo_models.CITaskAndroidStep().step_id)

class CITaskGATAPIStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskGATAPITestStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskGATAPIStepSerializer(instance=mongo_models.CITaskGATAPITestStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data

    def step_id(self):
        return str(mongo_models.CITaskGATAPITestStep().step_id)

class CITaskCommandStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskCommandStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskCommandStepSerializer(instance=mongo_models.CITaskCommandStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data


    def step_id(self):
        return str(mongo_models.CITaskCommandStep().step_id)


class CITaskGATUIStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskGATUITestStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)

    def to_json(self):

        serializer = CITaskGATUIStepSerializer(instance=mongo_models.CITaskGATUITestStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data
    def step_id(self):
        return str(mongo_models.CITaskGATUITestStep().step_id)

class CITaskStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskStep
        exclude = ('is_active','create_time')
        read_only_fields = ('id',)

class CITaskSSHStepSerializer(DocumentSerializer):

    class Meta:
        model = mongo_models.CITaskSSHStep
        exclude = ('is_active','create_time','id')
        read_only_fields = ('id',)


    def to_json(self):

        serializer = CITaskSSHStepSerializer(instance=mongo_models.CITaskSSHStep())
        parent_step = mongo_models.CITaskStep()
        parent_step.step_config = serializer.data
        parent_serializer = CITaskStepSerializer(instance=parent_step)
        return parent_serializer.data

    def step_id(self):
        return str(mongo_models.CITaskSSHStep().step_id)


