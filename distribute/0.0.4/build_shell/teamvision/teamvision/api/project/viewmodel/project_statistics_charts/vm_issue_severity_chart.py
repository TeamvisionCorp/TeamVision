#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from teamvision.project.models import Version,ProjectIssueSeverity
from teamvision.api.project.viewmodel.project_statistics_charts.vm_issue_property_chart import IssuePropertyChart
from business.project.issue_statistics_service import IssueStatisticsService
from business.auth_user.user_service import UserService


class IssueSeverityChart(IssuePropertyChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id):
        '''
        Constructor
        '''
        IssuePropertyChart.__init__(IssuePropertyChart,project_id,version_id,ProjectIssueSeverity,1)
        self.dimension=1
        self.chart_id=1
        self.chart_type='pie'
        self.chart_title="问题严重性分布"
        self.chart_sub_title="问题严重性占比"
        self.series_data=self.series()
    
    def chart_xaxis(self):
        property_name=list()
        property_values=self.property_values(self)
        for property_value in property_values:
            dm_property=ProjectIssueSeverity.objects.get_byvalue(property_value)
            if dm_property:
                property_name.append(dm_property.Name)
        return property_name
        
    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def get_property_issue(self,column_name):
        result=list()
        property_issue_list=IssueStatisticsService.issue_count_byproperty(self.project_id,self.version_id,self.dimension)
        for data in property_issue_list:
            temp=list()
            property_name=ProjectIssueSeverity.objects.get_byvalue(data['DimensionValue']).Name
            temp.append(property_name)
            temp.append(data['TotalCount']) 
            result.append(temp)
        print(result)
        return result
    
    
        
        
            
        