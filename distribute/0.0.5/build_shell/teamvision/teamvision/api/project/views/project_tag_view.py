# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status,response
from teamvision.api.project.serializer import project_serializer
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.filters.project_filter import ProjectTagFilterSet
from rest_framework.permissions import AllowAny
from teamvision.project.models import Tag


class ProjectTagListView(generics.ListCreateAPIView):

    '''
    get: /api/project/tags
    FilterSet: TagType: 1 通用,2 项目任务，3 Agent Operation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    '''

    serializer_class = project_serializer.ProjectTagSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]

    def get_queryset(self):
        tag_list = Tag.objects.all()
        return ProjectTagFilterSet(data=self.request.GET, queryset=tag_list).filter()


class PorjectTagView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = project_serializer.ProjectTagSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]

    def get_object(self):
        tag_id = int(self.kwargs['id'])
        tag = Tag.objects.get(tag_id)
        tag.IsActive = True
        return tag

