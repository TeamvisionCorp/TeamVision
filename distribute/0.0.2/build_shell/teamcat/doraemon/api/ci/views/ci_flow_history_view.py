#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from doraemon.api.ci.serializer import ci_taskflow_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import CITaskFlowHistory,CIFlowSectionHistory
from rest_framework.response import Response
from business.ci.ci_taskflow_service import CITaskFlowService
from business.ci.ci_taskflow_section_service import CITaskFlowSectionService
from doraemon.api.ci.filters.ci_pagination import CIPagination
from doraemon.api.ci.filters import ci_taskflow_filter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from gatesidelib.common.simplelogger import SimpleLogger





class CITaskFlowHistoryListView(generics.ListCreateAPIView):
    """
    get:
        get all ci taskflow history
        FilterSet: id,Status,TQUUID,TaskFlow
        FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        create new ci taskflow history
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowHistorySerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        flow_id = self.kwargs.get('flow_id')
        qs = CITaskFlowHistory.objects.flow_history(flow_id)
        return ci_taskflow_filter.CITaskFlowHistoryFilterSet(data=self.request.GET, queryset=qs).filter().order_by('-id')

class CITaskFlowHistoryView(generics.RetrieveUpdateAPIView):
    """
    /api/ci/flow_history/id
    get,update,task_flowhistory with id
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowHistorySerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_object(self):
        history_id = int(self.kwargs.get('id'))
        flow_history = CITaskFlowHistory.objects.get(history_id)
        return flow_history



class CIFlowSectionHistoryListView(generics.ListCreateAPIView):
    """
    get:
        get all ci section history
        FilterSet: id, TaskFlow,TaskFlowHistory,Status,TQUUID
        FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        create new ci section history
    """
    serializer_class = ci_taskflow_serializer.CIFlowSectionHistorySerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        flow_history_id = self.kwargs.get('flow_history_id')
        qs = CIFlowSectionHistory.objects.flow__section_history(flow_history_id)
        return ci_taskflow_filter.CIFlowSectionHistoryFilterSet(data=self.request.GET, queryset=qs).filter()

class CIFlowSectionHistoryView(generics.RetrieveUpdateAPIView):
    """
    /api/ci/section_history/id
    get,update,section history with id
    """
    serializer_class = ci_taskflow_serializer.CIFlowSectionHistorySerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_object(self):
        history_id = int(self.kwargs.get('id'))
        section_history = CIFlowSectionHistory.objects.get(history_id)
        return section_history











    



