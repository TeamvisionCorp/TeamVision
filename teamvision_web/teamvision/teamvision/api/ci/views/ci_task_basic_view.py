#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITask
from rest_framework.response import Response
from business.ci.ci_task_service import CITaskService
from teamvision.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.filters.ci_task_filter import CITaskFilterSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.redis_service import RedisService
from business.project.project_service import ProjectService




class CITaskBasicView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
         path:/api/ci/task_basic/<id>/
         id:taskid
    put:
         path:/api/ci/task_basic/<id>/
         id:taskid
    """
    serializer_class = ci_serializer.CITaskSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    

    def get_object(self):
        result_id =int(self.kwargs['id'])
        return CITask.objects.get(result_id)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CITaskOperationView(generics.RetrieveAPIView):
    """
    path:/api/ci/task_basic/<id>/<operation>?BuildParameter/TaskUUID
    id:taskid
    operation:start,stop,prelog
    BuildParameter: 可选,
    TaskUUID: operation 为stop时必选
    """
    serializer_class = ci_serializer.CITaskSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_object(self):
        result_id =int(self.kwargs['id'])
        return CITask.objects.get(result_id)

    def get(self,request, *args, **kwargs):
        task_id =int(self.kwargs['id'])
        operation = self.kwargs['operation'].strip(' ')
        build_parameter = self.request.GET.get('BuildParameter',None)
        task_uuid = self.request.GET.get('TaskUUID',None)
        task_queueid = self.request.GET.get('TQID',None)
        result = [0,'任务'+ str(task_id) +'指令下发失败，请联系管理员或者重试！']
        try:
            if operation == 'start':
                result = CITaskService.start_ci_task(request,task_id,build_parameter,0)
            if operation == 'stop' and task_uuid:
                result = CITaskService.stop_ci_task(request,task_id)
            if operation == 'prelog' and task_queueid:
                result = RedisService.get_value("ci_build_log"+str(task_queueid))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return Response({'tqid': result[0], 'message': result[1],'TaskUUID': result[2]})






class CITaskBasicListView(generics.ListCreateAPIView):
    """
    get:
        get all ci task list with project_id
        FilterSet: id, Project,TaskType,Schedule FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        and create new ci task
    """
    serializer_class = ci_serializer.CITaskSerializer
    permission_classes=[AllowAny]
    queryset=CITask.objects.all().filter(IsActive=1)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        qs = super(CITaskBasicListView, self).get_queryset().filter(IsActive=1)
        return CITaskFilterSet(data=self.request.GET, queryset=qs).filter()


    def create(self, request, *args, **kwargs):
        ci_task = CITaskService.create_ci_task(request.data,request.user)
        serializer = ci_serializer.CITaskSerializer(instance=ci_task,data = request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CITaskMyListView(generics.ListAPIView):
    """
    get:
        /api/ci/task_basic/my get all my ci task list
        FilterSet: Project,TaskType FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = ci_serializer.CITaskSerializer
    permission_classes=[AllowAny]
    queryset=CITask.objects.all().filter(IsActive=1)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = CIPagination

    def get_queryset(self):
        qs = CITaskService.get_product_ci_tasks(self.request,0,'all')
        return CITaskFilterSet(data=self.request.GET, queryset=qs).filter()


class CIMyProjectView(generics.ListAPIView):
    """
    get:
        get all ci task list with project_id
        FilterSet: Null FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_serializer.CIProjectSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        qs =ProjectService.get_projects_include_me(self.request)
        return qs






    



