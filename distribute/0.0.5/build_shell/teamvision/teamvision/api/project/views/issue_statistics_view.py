#coding=utf-8
# coding=utf-8
'''
Created on 2018-1-5

@author: zhangtiande
'''
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from teamvision.api.project.filters.issue_daily_statistics_filter import IssueDailyStatisticsFilterSet, \
    IssueVersionStatisticsFilterSet
from teamvision.api.project.serializer import project_issue_statistics_serializer
from teamvision.api.project.viewmodel.project_statistics_charts.vm_issue_category_chart import IssueCategoryChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_issue_resolve_result_chart import \
    IssueResolveResultChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_issue_severity_chart import IssueSeverityChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_module_issue_column_chart import \
    ModuleIssueColumnChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_new_issue_trend_chart import NewIssueTrendChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_total_issue_trend_chart import TotalIssueTrendChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_unclosed_issue_column_chart import \
    UnClosedIssueColumnChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_version_issue_column_chart import \
    VersionIssueColumnChart
from teamvision.project import models


class IssueTrendNew(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_trend_new
    获取每日新增以及解决的bug趋势图
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=NewIssueTrendChart(project_id,version_id,create_daterange)
        return chart


class IssueTrendTotal(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_trend_total
    获取项目新增以及解决的bug整体趋势图
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=TotalIssueTrendChart(project_id,version_id,create_daterange)
        return chart

class IssueTotalByVersion(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/statistics/version_issue_total
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=VersionIssueColumnChart(project_id,0,create_daterange)
        return chart

class UnclosedIssueByPeople(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/unclosed_issue
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=UnClosedIssueColumnChart(project_id,version_id,create_daterange)
        return chart
    
class IssueCountPerModule(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_count_per_module
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=ModuleIssueColumnChart(project_id,version_id,create_daterange)
        return chart
    
class IssueCountBySeverity(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_count_by_severity
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=IssueSeverityChart(project_id,version_id,create_daterange)
        return chart


class IssueCountByCategory(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_count_by_category
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=IssueCategoryChart(project_id,version_id,create_daterange)
        return chart

class IssueCountByResolveResult(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/issue_count_by_resolveresult
    获取项目个版本问题总数
    """
    serializer_class = project_issue_statistics_serializer.IssueTrendStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        create_daterange = self.request.GET.get('CreationTime', None)
        chart=IssueResolveResultChart(project_id,version_id,create_daterange)
        return chart

class IssueDailyStatisticsListView(generics.ListCreateAPIView):
    """
    /api/project/issue/daily_statistics
    FilterSet:['ProjectID','VersionID','StatisticsDate']
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = project_issue_statistics_serializer.IssueDailyStatisticsSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueDailyStatistics.objects.all()

    def get_queryset(self):
        qs = super(IssueDailyStatisticsListView, self).get_queryset()
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        if project_id!=0:
            qs=qs.filter(ProjectID=project_id)
        if version_id!=0:
            qs=qs.filter(VersionID=version_id)
        return IssueDailyStatisticsFilterSet(data=self.request.GET, queryset=qs).filter()

class IssueDailyStatisticsView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/issue/daily_statistics/id
    每日新增问题统计，以及查询
    """
    serializer_class = project_issue_statistics_serializer.IssueDailyStatisticsSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)

    def get_object(self):
        ds_id=self.kwargs.get('id',0)
        return models.ProjectIssueDailyStatistics.objects.get(ds_id)


class IssueVersionStatisticsListView(generics.ListCreateAPIView):
    """
    /api/project/issue/version_statistics
    FilterSet: ['ProjectID','VersionID','Dimension','DimensionValue']
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = project_issue_statistics_serializer.IssueVersionStatisticsSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueVersionStatistics.objects.all()

    def get_queryset(self):
        qs = super(IssueVersionStatisticsListView, self).get_queryset()
        return IssueVersionStatisticsFilterSet(data=self.request.GET, queryset=qs).filter()

class IssueVersionStatisticsView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/version_statistics/id
    get,update,delete with id
    """
    serializer_class = project_issue_statistics_serializer.IssueVersionStatisticsSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)

    def get_object(self):
        vs_id=self.kwargs.get('id',0)
        return models.ProjectIssueVersionStatistics.objects.get(vs_id)


class IssueStatusCountStatisticsView(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/status_summary
    """
    serializer_class = project_issue_statistics_serializer.IssueStatusSummaryCountSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_object(self):
        result = {}
        create_daterange = self.request.GET.get('CreationTime',None)
        project_id = self.kwargs.get('project_id', 0)
        version_id = self.kwargs.get('version_id', 0)
        result['project_id'] = project_id
        result['version_id'] = version_id
        result['daterange'] = create_daterange
        return result
