#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers

from business.project.issue_statistics_service import IssueStatisticsService
from teamvision.project.models import ProjectIssueDailyStatistics, ProjectIssueVersionStatistics


class IssueTrendStatisticsSerializer(serializers.Serializer):
    chart_id=serializers.IntegerField()
    project_id=serializers.IntegerField()
    version_id=serializers.IntegerField()
    chart_type=serializers.CharField()
    chart_title=serializers.CharField()
    chart_sub_title=serializers.CharField()
    xaxis=serializers.ListField()
    yaxis=serializers.ListField()
    tooltip=serializers.CharField()
    series_data=serializers.ListField()
    
    def save(self):
        raise Exception("only get request")


class IssueStatusSummaryCountSerializer(serializers.Serializer):
    newIssueCount = serializers.SerializerMethodField(method_name='new_issue_count')
    reslovedIssueCount = serializers.SerializerMethodField(method_name='resloved_issue_count')
    reopenedIssueCount = serializers.SerializerMethodField(method_name='reopened_issue_count')
    closedIssueCount = serializers.SerializerMethodField(method_name='closed_issue_count')

    def new_issue_count(self, obj):
        return IssueStatisticsService.issue_count_bystatus(obj['project_id'], obj['version_id'], 2,obj['daterange'])

    def resloved_issue_count(self, obj):
        return IssueStatisticsService.issue_count_bystatus(obj['project_id'], obj['version_id'], 4,obj['daterange'])

    def reopened_issue_count(self, obj):
        return IssueStatisticsService.issue_count_bystatus(obj['project_id'], obj['version_id'], 5,obj['daterange'])

    def closed_issue_count(self, obj):
        return IssueStatisticsService.issue_count_bystatus(obj['project_id'], obj['version_id'], 3,obj['daterange'])


class IssueDailyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueDailyStatistics
        exclude=('IsActive',)
        read_only_fields = ('id',)

class IssueVersionStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueVersionStatistics
        exclude=('IsActive',)
        read_only_fields = ('id',)
        
        
        