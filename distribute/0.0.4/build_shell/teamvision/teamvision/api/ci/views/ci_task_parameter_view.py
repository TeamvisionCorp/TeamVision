#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.mongo_models import CITaskParameterGroup
from business.ci.ci_task_parameter_service import CITaskParameterService


class CITaskParameterGroupView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.TaskParameterGroupSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        group_id =self.kwargs['id']
        return CITaskParameterService.task_parameter(group_id)

class CITaskParameterGroupListView(generics.ListCreateAPIView):
    """
    Parameter id:  TaskID
    """
    serializer_class = ci_serializer.TaskParameterGroupSerializer
    permission_classes=[AllowAny]
    

    def get_queryset(self):
        task_id=self.kwargs['task_id']
        return CITaskParameterService.task_parameter_list(task_id)
        

