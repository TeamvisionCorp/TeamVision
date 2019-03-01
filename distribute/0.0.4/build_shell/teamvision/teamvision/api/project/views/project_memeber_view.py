# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.project.models import ProjectMember, Project,Product
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from business.project.project_service import ProjectService
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from rest_framework.response import Response


class ProjectMemberListView(generics.ListCreateAPIView):
    """ 
    id:ProjectID
    """
    serializer_class = project_serializer.ProjectMemberSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        print(self.request.GET)
        print(self.kwargs)
        project_id = int(self.kwargs.get('project_id',0))
        if str(project_id) == "0":
            project_id = self.request.GET.get("project_id")
        memberList = ProjectMember.objects.get_members(project_id)
        return memberList


class PorjectMemberView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = project_serializer.ProjectMemberSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        member_id = int(self.kwargs['id'])
        member = ProjectMember.objects.get(member_id)
        return ProjectMember(member)


class ProjectListView(generics.ListCreateAPIView):
    """
    api: /api/project/list?extinfo=1&my=1

    extinfo: 0|1

    my: return project list with login user
    """
    serializer_class = project_serializer.ProjectSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        show_extinfo = self.request.GET.get('extinfo',0)
        latest = self.request.GET.get('latest',0)
        my=self.request.GET.get('my',0)
        project_list = Project.objects.all()
        if str(my)=='1':
            project_list=ProjectService.get_projects_include_me(self.request)
            if str(latest) == '1':
                project_list=ProjectService.get_latest_projects_include_me(self.request)
        return project_list

    def create(self, request, *args, **kwargs):
        project = ProjectService.create_project(request)
        serializer = project_serializer.ProjectSerializer(instance=project,data = request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/{id}/detail?extinfo=1     extinfo:1/0
    """
    serializer_class = project_serializer.ProjectSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_object(self):
        project_id = int(self.kwargs['id'])
        show_extinfo = self.request.GET.get('extinfo',0)
        project = Project.objects.get(project_id)
        return project


class ProductListView(generics.ListAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = project_serializer.ProductSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Product.objects.all()
