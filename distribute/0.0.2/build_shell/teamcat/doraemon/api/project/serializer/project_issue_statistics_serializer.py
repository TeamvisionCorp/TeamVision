#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from doraemon.project.models import ProjectIssueDailyStatistics,ProjectIssueVersionStatistics



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
        
        
        