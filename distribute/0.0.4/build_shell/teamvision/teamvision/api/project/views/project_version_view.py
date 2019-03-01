#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.project.models import Version
from teamvision.api.project.render import project_version_render




class ProjectVersionListView(generics.ListCreateAPIView):
    """ 
    id:ProjectID
    """
    serializer_class = project_serializer.ProjectVersionSerializer
    permission_classes=[AllowAny]
    renderer_classes = [project_version_render.ProjectVersionListRenderer]
    

    def get_queryset(self):
        print(self.kwargs)
        project_id =int(self.kwargs['project_id'])
        return Version.objects.get_versions(project_id)

class ProjectVersionView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = project_serializer.ProjectVersionSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        version_id =int(self.kwargs['id'])
        return Version.objects.get(version_id)

    

    