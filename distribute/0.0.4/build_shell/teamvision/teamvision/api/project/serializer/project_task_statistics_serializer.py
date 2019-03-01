#coding=utf-8
'''
Created on 2018-12-13

@author: zhangtiande
'''

from rest_framework import serializers



class TaskTrendStatisticsSerializer(serializers.Serializer):
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


class TaskPieStatisticsSerializer(serializers.Serializer):
    chart_id = serializers.IntegerField()
    project_id = serializers.IntegerField()
    version_id = serializers.IntegerField()
    chart_type = serializers.CharField()
    chart_title = serializers.CharField()
    show_legend = serializers.BooleanField()
    series_name = serializers.CharField()
    series_data = serializers.ListField()

    def save(self):
        raise Exception("only get request")

class TaskSummaryStatisticsSerializer(serializers.Serializer):
    chart_id = serializers.IntegerField()
    project_id = serializers.IntegerField()
    version_id = serializers.IntegerField()
    today_finished_count = serializers.IntegerField()
    delayed_count = serializers.IntegerField()
    delay_finished_count = serializers.IntegerField()

    def save(self):
        raise Exception("only get request")
        
        
        