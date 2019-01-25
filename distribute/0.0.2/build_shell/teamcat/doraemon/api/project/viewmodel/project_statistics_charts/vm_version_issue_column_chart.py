#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from doraemon.project.models import Version
from doraemon.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart
from business.project.issue_statistics_service import IssueStatisticsService


class VersionIssueColumnChart(VM_HighChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id,date_range=30):
        '''
        Constructor
        '''
        VM_HighChart.__init__(VersionIssueColumnChart,project_id, version_id)
        self.chart_id=1
        self.chart_type="column"
        self.chart_title="问题数量"
        self.chart_sub_title="项目个版本问题"
        self.xaxis=self.chart_xaxis()
        self.yaxis=self.chart_yaxis()
        self.yaxis_title=""
        self.tooltip=self.chart_tooltip()
        self.series_data=self.series()
    
    def chart_xaxis(self):
        result=list()
        version_data=IssueStatisticsService.issue_count_byversion(self.project_id)
        for data in version_data:
            dm_version=Version.objects.get(data['VersionID'])
            result.append(dm_version.VVersion)
        return result
    
    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def series(self):
        result=list()
        total_issue=self.get_issue_total(self.chart_title)
        result.append(total_issue)
        return result
    
    def get_issue_total(self,trend_name):
        result=dict()
        result['name']=trend_name
        result['data']=list()
        all_version_issue_count=IssueStatisticsService.issue_count_byversion(self.project_id)
        for data in all_version_issue_count:
            result['data'].append(data['TotalCount'])
        return result
        
            
        