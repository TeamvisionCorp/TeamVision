#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.project.models import ProjectIssueDailyStatistics,ProjectIssueVersionStatistics
from url_filter.filtersets.django import ModelFilterSet

class IssueDailyStatisticsFilterSet(ModelFilterSet):
    class Meta(object):
        model = ProjectIssueDailyStatistics
        fields = ['ProjectID','VersionID','StatisticsDate']

class IssueVersionStatisticsFilterSet(ModelFilterSet):
    class Meta(object):
        model = ProjectIssueVersionStatistics
        fields = ['ProjectID','VersionID','Dimension','DimensionValue']


        