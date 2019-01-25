#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from doraemon.api.ci.serializer import ci_taskflow_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import CITaskFlow,CITaskFlowSection
from doraemon.api.ci.viewmodel.api_ci_taskflow import ApiCITaskFlow
from rest_framework.response import Response
from business.ci.ci_taskflow_service import CITaskFlowService
from business.ci.ci_taskflow_section_service import CITaskFlowSectionService
from doraemon.api.ci.filters.ci_pagination import CIPagination
from doraemon.api.ci.filters.ci_taskflow_filter import CITaskFlowFilterSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from gatesidelib.common.simplelogger import SimpleLogger




class CITaskFlowView(generics.RetrieveUpdateDestroyAPIView):
    """
    path:/api/ci/task_flow/<id>/
    id:taskid
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    

    def get_object(self):
        taskflow_id = int(self.kwargs['id'])
        print(taskflow_id)
        task_flow=CITaskFlow.objects.get(taskflow_id)
        temp=ApiCITaskFlow(task_flow)
        task_flow.Sections=temp.Sections
        return task_flow

    def delete(self,request, *args, **kwargs):
        flow_id =int(kwargs['id'])
        task_flow=CITaskFlow.objects.get(flow_id)
        result = '任务流 ['+ task_flow.FlowName +'] 删除失败，请联系管理员或者重试！'
        try:
            result = CITaskFlowService.delete_taskflow(request.user,flow_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return Response({'message': result})


class CITaskFlowOperationView(generics.RetrieveAPIView):
    """
    path:/api/ci/task_flow/<id>/<operation>
    id:taskflow id
    operation:start,copy
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        flow_id = int(self.kwargs['id'])
        task_flow=CITaskFlow.objects.get(flow_id)
        return task_flow

    def get(self,request, *args, **kwargs):
        flow_id =int(kwargs['id'])
        task_flow=CITaskFlow.objects.get(flow_id)
        operation = kwargs['operation'].strip()
        result = '任务流 ['+ task_flow.FlowName +'] 执行指令下发失败，请联系管理员或者重试！'
        try:
            if operation == 'start':
                result = CITaskFlowService.start_taskflow(request,flow_id)
            if operation == 'copy':
                result = CITaskFlowService.copy_taskflow(request.user,flow_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return Response({'message': result})



class CITaskFlowListView(generics.ListCreateAPIView):
    """
    /api/ci/task_flow/list
    get all ci taskflow  and create new ci task
    FilterSet: id, Project
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowListSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        qs = CITaskFlow.objects.all().filter(IsActive=1)
        return CITaskFlowFilterSet(data=self.request.GET, queryset=qs).filter()

    def create(self, request, *args, **kwargs):
        task_flow = CITaskFlowService.create_taskflow(request.data,request.user)
        serializer = ci_taskflow_serializer.CITaskFlowListSerializer(instance=task_flow,data = request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CITaskFlowMyListView(generics.ListAPIView):
    """
    /api/ci/task_flow/my get all my ci taskflow FilterSet:id,Project FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowListSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        qs = CITaskFlowService.get_my_taskflows(self.request,'all')
        return CITaskFlowFilterSet(data=self.request.GET, queryset=qs).filter()


class CITaskFlowSectionView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/ci/task_flow/section/id
    get,update,delete section with section id
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowSectionSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_object(self):
        section_id = int(self.kwargs.get('id', 0))
        section = CITaskFlowSection.objects.get(section_id)
        return section

class CIFlowSectionOperationView(generics.RetrieveAPIView):
    """
    path:/api/ci/flow_section/<id>/<operation>
    id:section id
    operation:start
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowSectionSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_object(self):
        section_id = int(self.kwargs.get('id', 0))
        section = CITaskFlowSection.objects.get(section_id)
        return section

    def get(self,request, *args, **kwargs):
        section = self.get_object()
        operation = kwargs['operation'].strip()
        result = '任务流阶段 ['+ section.SectionName +'] 执行指令下发失败，请联系管理员或者重试！'
        try:
            if operation == 'start':
                result = CITaskFlowSectionService.start_flowsection(request,section.id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return Response({'message': result})

class CITaskFlowSectionListView(generics.ListCreateAPIView):
    """
    /api/ci/task_flow_section/id
    get,update,delete section with section id
    """
    serializer_class = ci_taskflow_serializer.CITaskFlowSectionSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        flow_id = int(self.kwargs.get('flow_id', 0))
        sections = CITaskFlowSection.objects.flow_sections(flow_id).order_by('SectionOrder')
        return sections







    



