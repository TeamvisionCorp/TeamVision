#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from doraemon.api.ci.serializer import autotesting_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import AutoTestingTaskResult
# from business.ci.ci_task_history_service import CITaskHistoryService
# from rest_framework.response import Response
from doraemon.api.ci.filters.ci_pagination import CIPagination
from doraemon.api.ci.filters.auto_testing_result_filter import AutoTestingResultFilterSet


class AutoTestingResultView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = autotesting_serializer.AutoTestingTaskResultSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        result_id =int(self.kwargs['id'])
        return AutoTestingTaskResult.objects.get(result_id)



class AutoTestingResultListView(generics.ListCreateAPIView):
    """
    /api/ci/auto_testing_results
    FilterSet: TaskHistoryID,TaskUUID
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = autotesting_serializer.AutoTestingTaskResultSerializer
    permission_classes=[AllowAny]
    queryset=AutoTestingTaskResult.objects.all()
    pagination_class = CIPagination
    
    def get_queryset(self):
        qs = super(AutoTestingResultListView, self).get_queryset()
        return AutoTestingResultFilterSet(data=self.request.GET, queryset=qs).filter()
    



