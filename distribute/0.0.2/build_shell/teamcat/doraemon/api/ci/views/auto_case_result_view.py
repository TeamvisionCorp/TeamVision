#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from doraemon.api.ci.serializer import autotesting_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import AutoCaseResult,UnitTestCaseResult
from doraemon.api.ci.filters.ci_pagination import CIPagination
from doraemon.api.ci.filters.auto_case_result_filter import AutoCaseResultFilterSet,UnitTestCaseResultFilterSet


class AutoTestingCaseResultView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = autotesting_serializer.AutoCaseResultSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        result_id =int(self.kwargs['id'])
        return AutoCaseResult.objects.get(result_id)



class AutoTestingCaseResultListView(generics.ListCreateAPIView):
    """
    /api/ci/auto_testing_results?TaskResultID=1446: return results with TaskResultID 1446
    /api/ci/auto_testing_results return all
    """
    serializer_class = autotesting_serializer.AutoCaseResultSerializer
    permission_classes=[AllowAny]
    queryset=AutoCaseResult.objects.all()
    pagination_class = CIPagination
    
    def get_queryset(self):
        qs = super(AutoTestingCaseResultListView, self).get_queryset()
        return AutoCaseResultFilterSet(data=self.request.GET, queryset=qs).filter()


class UnitTestCaseResultView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = autotesting_serializer.UnitTestCaseResultSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        print(self.request.data)
        result_id =int(self.kwargs['id'])
        return UnitTestCaseResult.objects.get(result_id)



class UnitTestCaseResultListView(generics.ListCreateAPIView):
    """
    /api/ci/auto_unittest_results?TaskResultID=1446: return results with TaskResultID 1446
    /api/ci/auto_unittest_results return all
    """
    serializer_class = autotesting_serializer.UnitTestCaseResultSerializer
    permission_classes=[AllowAny]
    queryset=UnitTestCaseResult.objects.all()
    pagination_class = CIPagination
    
    def get_queryset(self):
        qs = super(UnitTestCaseResultListView, self).get_queryset()
        return UnitTestCaseResultFilterSet(data=self.request.GET, queryset=qs).filter()
    



