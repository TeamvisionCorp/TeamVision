# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.project.models import ProjectModule


class ProjectModuleListView(generics.ListCreateAPIView):
    """ 
    id:ProjectID
    """
    serializer_class = project_serializer.ProjectModuleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        project_id = int(self.kwargs['project_id'])
        module_list = ProjectModule.objects.project_modules(project_id)
        return module_list


class PorjectModuleView(generics.RetrieveUpdateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = project_serializer.ProjectMemberSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        module_id = int(self.kwargs['id'])
        module = ProjectModule.objects.get(module_id)
        return module
