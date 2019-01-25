#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.datetimehelper import DateTimeHelper
from doraemon.project.models import Version, ProjectIssue,ProjectIssueDailyStatistics,ProjectIssueVersionStatistics
from business.project.issue_service import IssueService
from django.db.models import Sum,Count


class IssueStatisticsService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def issue_trend_last30days(project_id,version_id):
        result=ProjectIssueDailyStatistics.objects.get_project_issue_statistics(int(project_id)).values('StatisticsDate').annotate(OpenedToday=Sum('OpenedToday'),ResolvedToday=Sum('FixedToday'),OpenedTotal=Sum('OpenedTotal'),ResolvedTotal=Sum('FixedTotal'))
        if str(version_id)!="0":
            tmp_version = Version.objects.get(int(version_id))
            result=result.filter(VersionID=int(version_id))
            if tmp_version.VStartDate and tmp_version.VReleaseDate:
                result = result.filter(StatisticsDate__range=(tmp_version.VStartDate,tmp_version.VReleaseDate))
        if len(result)>=30:
            return result.order_by('StatisticsDate')[len(result)-30:]
        else:
            return result.order_by('StatisticsDate')

    @staticmethod
    def issue_count_bystatus(project_id,version_id,status):
        result=IssueService.project_all_issues(project_id)
        if str(version_id)!="0":
            result=result.filter(Version=int(version_id))
        return result.filter(Status=int(status)).count()
    
    @staticmethod
    def issue_count_byversion(project_id):
        result=ProjectIssueDailyStatistics.objects.get_project_issue_statistics(project_id).values('VersionID').annotate(TotalCount=Sum('OpenedToday'))
        return result
    
    
    @staticmethod
    def unclosed_issue_count(project_id,version_id,status=0):
        result=ProjectIssue.objects.get_project_issue(project_id)
        if str(version_id)!="0":
            result=result.filter(Version=int(version_id))
        if str(status)!="0":
            result=result.filter(Status=int(status))
        else:
            result=result.filter(Status__in=[2,5,4])
        result=result.values('Processor','Status').annotate(TotalCount=Count('id')).order_by('Processor')
        return result
    
    @staticmethod
    def issue_count_byproperty(project_id,version_id,dimension=0):
        result=ProjectIssueVersionStatistics.objects.get_project_issue_statistics(project_id)
        if str(version_id)!="0":
            result=result.filter(VersionID=int(version_id))
        if str(dimension)!="0":
            result=result.filter(Dimension=int(dimension))
        result=result.values('DimensionValue').annotate(TotalCount=Sum('IssueTotal')).order_by('DimensionValue')
        return result
    
    
  
            
            
        