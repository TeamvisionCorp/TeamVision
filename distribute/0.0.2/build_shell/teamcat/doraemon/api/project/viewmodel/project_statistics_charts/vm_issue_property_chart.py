#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from doraemon.project.models import Version,ProjectIssueSeverity
from doraemon.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart
from business.project.issue_statistics_service import IssueStatisticsService
from business.auth_user.user_service import UserService


class IssuePropertyChart(VM_HighChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id,model,dimension):
        '''
        Constructor
        '''
        VM_HighChart.__init__(IssuePropertyChart,project_id,version_id)
        self.dimension=dimension
        self.property_model=model
        self.xaxis=self.chart_xaxis(self)
        self.yaxis=self.chart_yaxis(self)
        self.yaxis_title=""
        self.tooltip=self.chart_tooltip(self)

     
    def chart_xaxis(self):
        property_name=list()
        property_values=self.property_values(self)
        for property_value in property_values:
            dm_property=self.property_model.objects.get_byvalue(property_value)
            if dm_property:
                property_name.append(dm_property.Name)
        return property_name
    
    def property_values(self):
        property_issue_list=IssueStatisticsService.issue_count_byproperty(self.project_id,self.version_id,self.dimension)
        property_values=list()
        for data in property_issue_list:
            if not data['DimensionValue'] in property_values:
                property_values.append(data['DimensionValue'])
        return property_values
        
    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def series(self):
        property_issue_count=self.get_property_issue('问题数量')
        result=property_issue_count
        return result
    
#     def get_property_issue(self,column_name):
#         result=list()
#         property_issue_list=IssueStatisticsService.issue_count_byproperty(self.project_id,self.version_id,self.dimension)
#         for data in property_issue_list:
#             temp=list()
#             print(data)
#             print(self.property_model)
#             property_name=self.property_model.objects.get_byvalue(data['DimensionValue']).Name
#             temp.append(property_name)
#             temp.append(data['TotalCount']) 
#             result.append(temp)
#         print(result)
#         return result
        
        
            
        