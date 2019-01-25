#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from gatesidelib.datetimehelper import DateTimeHelper
from doraemon.project.models import ProjectIssue
from doraemon.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart
from business.project.issue_statistics_service import IssueStatisticsService


class TotalIssueTrendChart(VM_HighChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id,date_range=30):
        '''
        Constructor
        '''
        VM_HighChart.__init__(TotalIssueTrendChart,project_id, version_id)
        self.chart_id=1
        self.chart_type="area"
        self.chart_title="问题数量"
        self.chart_sub_title="总体趋势"
        self.xaxis=self.chart_xaxis()
        self.yaxis=self.chart_yaxis()
        self.yaxis_title=""
        self.tooltip=self.chart_tooltip()
        self.series_data=self.series()
    
    def chart_xaxis(self):
        result=list()
        last30_days_data=IssueStatisticsService.issue_trend_last30days(self.project_id,self.version_id)
        for data in last30_days_data:
            result.append(data.get('StatisticsDate'))
        return result
    
    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def series(self):
        result=list()
        new_issue_trend=self.get_issue_trend("New")
        resolved_issue_trend=self.get_issue_trend("Resolved")
        result.append(new_issue_trend)
        result.append(resolved_issue_trend)
        return result
    
    def get_issue_trend(self,trend_name):
        result=dict()
        result['name']=trend_name
        result['data']=list()
        last30_days_data=IssueStatisticsService.issue_trend_last30days(self.project_id,self.version_id)
        if trend_name=="New":
            for data in last30_days_data:
                result['data'].append(data.get('OpenedTotal'))
        if trend_name=="Resolved":
            for data in last30_days_data:
                result['data'].append(data.get('ResolvedTotal'))
        return result
        
            
        