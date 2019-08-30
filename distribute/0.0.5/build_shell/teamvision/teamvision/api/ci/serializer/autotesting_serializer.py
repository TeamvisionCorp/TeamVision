#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.ci.models import AutoCase,AutoCaseResult,AutoTestingTaskResult,ServiceHost,UnitTestCaseResult


class AutoCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoCase
        exclude = ('CreateTime',)
        read_only_fields = ('id',)




class AutoCaseResultSerializer(serializers.ModelSerializer):
    TestCaseName=serializers.SerializerMethodField()
    CaseDesc = serializers.SerializerMethodField()
    ResultFormat = serializers.SerializerMethodField()
    Exception = serializers.SerializerMethodField()


    def get_CaseDesc(self,obj):
        result="--"
        if obj.TestCaseID:
            auto_test_case=AutoCase.objects.get(obj.TestCaseID)
            if auto_test_case:
                result=auto_test_case.Desc
            else:
                result = '--'
        return result

    def get_ResultFormat(self,obj):
        result="--"
        if obj.Result:
            if obj.Result == 3:
                result = "Pass"
            elif obj.Result == 2:
                result = "Fail"
            else:
                result = "Aborted"
        return result

    def get_Exception(self,obj):
        error = ""
        trace = ""
        if obj.Error:
            error = str(obj.Error)

        if obj.StackTrace:
            trace = str(obj.StackTrace)
        return error+"  "+trace

    def get_TestCaseName(self,obj):
        result="--"
        if obj.TestCaseID:
            auto_test_case=AutoCase.objects.get(obj.TestCaseID)
            if auto_test_case:
                result=auto_test_case.ClassName+'.'+auto_test_case.CaseName
            else:
                result = '--'
        return result
              
    class Meta:
        model = AutoCaseResult
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)


class UnitTestCaseResultSerializer(serializers.ModelSerializer):   
    class Meta:
        model = UnitTestCaseResult
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)
        

class AutoTestingTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoTestingTaskResult
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)
        
class ServiceHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHost
        exclude = ('CreateTime','IsActive')
        read_only_fields = ('id',)

