#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from doraemon.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from doraemon.api.project.filters import project_issue_filter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.project import models
from mongoengine import queryset




class IssueView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/issue/issue_id
    update,get,delete issue  with issue_id
    """
    serializer_class = project_serializer.ProjectIssueSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    

    def get_object(self):
        issue_id=self.kwargs.get('issue_id',0)
        return models.ProjectIssue.objects.get(issue_id)

class IssueListView(generics.ListCreateAPIView):
    """
    get:
        /api/project/project_id/version_id/issues
        get issue list with project_id,version_id
        FilterSet: ['Project','Version','Status','Module','Processor','IssueCategory','Solution','Severity','Creator','CreationTime','ClosedTime','ResolvedTime']
        FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        create new issue
    """
    serializer_class = project_serializer.ProjectIssueSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssue.objects.all()
    
    def get_queryset(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        qs = super(IssueListView, self).get_queryset()
        if str(project_id)!="0":
            qs=qs.filter(Project=project_id)
        if str(version_id)!="0":
            qs=qs.filter(Version=version_id)
        return project_issue_filter.IssueDailyStatisticsFilterSet(data=self.request.GET, queryset=qs).filter()



class IssueStatusList(generics.ListAPIView):
    """
    /api/project/issue/status
    获取问题状态列表
    """
    serializer_class = project_serializer.ProjectIssueStatuserializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueStatus.objects.all()

class IssueSeverityList(generics.ListAPIView):
    """
    /api/project/issue/severities
    获取问题状态列表
    """
    serializer_class = project_serializer.ProjectIssueSeveritySerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueSeverity.objects.all()

class IssueCategoryList(generics.ListAPIView):
    """
    /api/project/issue/categories
    获取问题分类列表
    """
    serializer_class = project_serializer.ProjectIssueCategorySerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueCategory.objects.all()


class IssueResolveResultList(generics.ListAPIView):
    """
    /api/project/issue/resolve_results
    获取问题解决结果列表
    """
    serializer_class = project_serializer.ProjectIssueResolvedResultSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueResolvedResult.objects.all()

class ProjectModuleList(generics.ListAPIView):
    """
    /api/project/project_id/modules
    获取项目模块列表
    """
    serializer_class = project_serializer.ProjectModuleSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectModule.objects.all()
    
    def get_queryset(self):
        project_id=self.kwargs.get('project_id',0)
        qs=super(ProjectModuleList, self).get_queryset()
        if project_id:
            qs=qs.filter(ProjectID=project_id)
        return qs
    





    

    