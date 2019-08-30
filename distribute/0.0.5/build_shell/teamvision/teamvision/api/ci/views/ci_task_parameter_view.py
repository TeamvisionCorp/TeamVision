#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from rest_framework.response import Response
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.mongo_models import CITaskParameterGroup
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from business.ci.ci_task_parameter_service import CITaskParameterService


class CITaskParameterGroupView(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView):
    """
    get: /api/ci/task/parameter_group/<id>/

    put: /api/ci/task/parameter_group/<id>/

    patch: /api/ci/task/parameter_group/<id>/

    post: /api/ci/task/parameter_group/<id>/copy

    """
    serializer_class = ci_serializer.TaskParameterGroupSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    

    def get_object(self):
        group_id =self.kwargs['id']
        return CITaskParameterService.task_parameter(group_id)

    def put(self, request, *args, **kwargs):
        result = self.update(request, *args, **kwargs)
        group = self.get_object()
        if group.is_default:
            CITaskParameterService.set_parameter_group_default(group,True)
        return result

    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        group = self.get_object()
        if group.is_default:
            CITaskParameterService.set_parameter_group_default(group, True)
        return result

    def post(self, request, *args, **kwargs):
        group_id =self.kwargs['id']
        parameter_group = CITaskParameterService.copy_task_parameter(group_id)
        group_serializer = ci_serializer.TaskParameterGroupSerializer(instance=parameter_group)
        return Response(group_serializer.data)


class CITaskParameterGroupListView(generics.ListCreateAPIView):
    """
    Parameter id:  TaskID
    """
    serializer_class = ci_serializer.TaskParameterGroupSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        task_id=self.kwargs['task_id']
        return CITaskParameterService.task_parameter_list(task_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        CITaskParameterService.save_step_settings(serializer.instance.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

